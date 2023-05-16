"""/v1/task/{task_id}/ PUT handler."""

from typing import Any, Dict

from libs.task_service import TaskService
from libs.utils import LoggingService
from models.task import Task

logger = LoggingService.get_logger(__name__)


def handler(request_dict: Dict[str, Any]) -> Task:
    """Handle request.

    Args:
        request_dict (Dict[str, Any]): Request dictionary.

    Returns:
        Dict[str, Any]: Response dictionary.
    """

    new_task = Task(**request_dict)
    logger.debug("new_task: %s", new_task)

    task_service = TaskService()
    task = task_service.update_task(new_task)

    return task
