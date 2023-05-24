"""v1/hosts/{host_id} DELETE handler."""
from libs.host_service import HostService


def handler(host_id) -> None:
    """
    Deletes a host.
    """

    # delete host
    host_service = HostService()
    host_service.delete_host(host_id)

    return
