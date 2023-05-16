"""v1/hosts GET method handler"""
from typing import List

from libs.host_service import HostService
from libs.utils import LoggingService
from models.host import Host

logger = LoggingService.get_logger(__name__)


def handler() -> List[Host]:
    """GET all hosts"""

    logger.info("Getting hosts...")

    host_service = HostService()

    # get hosts
    hosts = host_service.get_hosts()

    return hosts
