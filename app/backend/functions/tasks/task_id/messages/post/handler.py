"""v1/tasks/{task_id}/messages/ POST handler."""
from libs.generative_cmd_service import GenerativeCmdService
from libs.task_service import MessageService, TaskService
from libs.utils import LoggingService
from models.task import HostMessage

logger = LoggingService.get_logger(__name__)


def handler(msg: HostMessage, task_id: str):
    """Handle request.

    Args:
        msg (HostMessage): Message from host.
        task_id (str): Task ID.

    Returns:
        task (Task): Task object
    """

    # get task
    logger.debug("Getting task...")
    task_service = TaskService()
    task = task_service.get_task(task_id)

    # add message from host
    logger.debug("Adding message...")
    message_service = MessageService()
    task = message_service.add_message(task, msg)

    # generate next command
    logger.debug("Generating next command...")
    generative_cmd_service = GenerativeCmdService()
    gpt_msg = generative_cmd_service.generate_cmd(task)
    task = message_service.add_message(task, gpt_msg)

    # return task
    logger.debug("Returning task...")
    return task
