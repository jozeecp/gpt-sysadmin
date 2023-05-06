"""Host service"""
import json
import os

from libs.base_service import BaseService
from libs.cmd_service import CmdService
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

        # quick SSH connection test
        logger.debug("Testing SSH connection...")
        test_result = CmdService.ssh_connection_test(host_create)
        if not test_result:
            # could not connect to host, will register key with password
            try:
                logger.debug(
                    "Could not connect to host, registering key with password..."
                )
                CmdService.register_ssh_key(host_create)
            except Exception as e:
                logger.error("Error registering key with password: %s", e)
                raise e

        # create host from host create
        host = Host(
            host_id=host_create.host_id,
            hostname=host_create.hostname,
            description=host_create.description,
            ip=host_create.ip,
            username=host_create.username,
        )

        # register host in redis
        self.redis_client.set(host.host_id, host.json())
        logger.debug("Host registered in redis: %s", host.json())

        return host

    def get_host(self, host_id: str) -> Host:
        """Get host from redis"""

        # get host from redis
        host_json = self.redis_client.get(host_id)
        host = Host(**json.loads(host_json))
        logger.debug("Host retrieved from redis: %s", host.dict())

        return host
