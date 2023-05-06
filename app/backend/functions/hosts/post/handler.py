"""Function to handle host creation"""
from typing import Any

from libs.host_service import HostService
from libs.utils import LoggingService
from models.host import HostCreate

logger = LoggingService.get_logger(__name__)


def handler(host: HostCreate) -> Any:
    """Handle host creation"""

    logger.info("Creating host...")
    logger.debug("Received host data: %s", host)

    host_service = HostService()

    # create host
    host_new = host_service.create_host(host)

    return host_new
