"""Host service"""
import json
import os
from typing import List

import requests
from libs.base_service import BaseService
from libs.utils import LoggingService
from models.host import Host, HostCreate

logger = LoggingService.get_logger(__name__)

redis_db = os.environ.get("HOST_REDIS_DB")


class HostService(BaseService):
    """Host service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def create_host(self, host_create: HostCreate) -> Host:
        """Create a new host"""

        # create host from host create
        host = Host(**host_create.dict())

        # register host in redis
        self.redis_client.set(host.host_id, host.json())
        logger.debug("Host registered in redis: %s", host.json())

        # if no ip, return early
        if not host.ip:
            return host

        # register host in DNS
        dns_api_url = "http://coredns-api:5001/hosts"
        dns_api_data = {
            "hostname": host.hostname,
            "ip": host.ip,
        }
        response = requests.post(dns_api_url, json=dns_api_data)
        assert response.status_code == 200, response.text

        return host

    def get_host(self, host_id: str) -> Host:
        """Get host from redis"""

        # get host from redis
        host_json = self.redis_client.get(host_id)
        host = Host(**json.loads(host_json))
        logger.debug("Host retrieved from redis: %s", host.dict())

        return host

    def get_hosts(self) -> List[Host]:
        """Get all hosts from redis"""

        # get all hosts from redis
        hosts = []
        for host_id in self.redis_client.keys():
            host_json = self.redis_client.get(host_id)
            try:
                host = Host(**json.loads(host_json))
                hosts.append(host)
            except ValueError:
                logger.error("Bad host: %s", host_json)
                logger.debug("Deleting bad host...")
                self.redis_client.delete(host_id)
                continue
        logger.debug("Hosts retrieved from redis: %s", hosts)

        return hosts

    def delete_host(self, host_id: str) -> None:
        """Delete a host from redis"""

        # if ip, delete host from DNS
        host = self.get_host(host_id)
        if host.ip:
            dns_api_url = f"http://coredns-api:5001/hosts/{host.ip}"
            response = requests.delete(dns_api_url)
            assert response.status_code == 200, response.text

        # delete host from redis
        self.redis_client.delete(host_id)
        logger.debug("Host deleted from redis.")
