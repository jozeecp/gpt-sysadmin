"""Function to handle host creation"""
from typing import Any

from models.host import Host
from libs.host_service import HostService

def handler(host: Host) -> Any:
    """Handle host creation"""

    host_service = HostService()

    # create host
    host_new = host_service.create_host(host)

    return host_new
