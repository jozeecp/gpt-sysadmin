"""/host/{host_id} GET method handler."""
from typing import Any

from libs.host_service import HostService
from libs.utils import LoggingService
from models.host import Host

logger = LoggingService.get_logger(__name__)

def handler(host_id: str) -> Host:
    """GET host"""

    logger.info("Getting host...")
    logger.debug("Received host ID: %s", host_id)

    host_service = HostService()

    # get host
    host = host_service.get_host(host_id)

    return host
