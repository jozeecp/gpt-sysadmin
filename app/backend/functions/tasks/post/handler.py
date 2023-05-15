"""Task creation handler"""
from libs.generative_cmd_service import GenerativeCmdService
from libs.task_service import MessageService, TaskService
from libs.utils import LoggingService
from models.task import Task

logger = LoggingService.get_logger(__name__)


def handler(task_old: Task) -> Task:
    """Handle task creation"""

    task_service = TaskService()
    message_service = MessageService()

    # create task
    logger.debug("task_old: %s", task_old)
    task_new = task_service.create_task(task_old)
    logger.debug("task_new: %s", task_new)

    # generate command
    logger.debug("generating command...")
    cmd = GenerativeCmdService().generate_cmd(task_new)
    logger.debug("cmd: %s", cmd)

    # add gpt message
    logger.debug("Adding message:", cmd.dict())
    message_service.add_message(task_new, cmd)

    # get latest task object
    task_final = task_service.get_task(task_new.taskId)
    logger.debug("task_final: %s", task_final)

    return task_final
