"""Host service"""
import os
import logging

from models.host import Host
from libs.base_service import BaseService

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

redis_db = os.environ.get("HOST_REDIS_DB")


class HostService(BaseService):
    """Host service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def create_host(self, host: Host) -> Host:
        """Create a new host"""

        # register host in redis
        self.redis_client.set(host.host_id, host.json())
        logger.debug("Host registered in redis: %s", host.json())

        return host
