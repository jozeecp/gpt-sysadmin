from libs.task_service import TaskService
from models.task import Task


def handler(task_id: str) -> Task:
    """Handle request."""

    # get task
    task_service = TaskService()
    task = task_service.get_task(task_id)

    # return task
    return task