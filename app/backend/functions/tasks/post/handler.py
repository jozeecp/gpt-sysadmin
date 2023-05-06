"""Task creation handler"""
from libs.cmd_service import CmdService
from libs.generative_cmd_service import GenerativeCmdService
from libs.task_service import MessageService, TaskService
from libs.utils import LoggingService
from models.task import HostMessage, Task

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
    cmd = GenerativeCmdService().generate_cmd(task_new)

    # add gpt message
    print("Adding message:", cmd)
    message_service.add_message(task_new, cmd)

    # run command
    cmd_service = CmdService(task_new)
    output = cmd_service.execute_command(cmd)

    # add host message
    host_msg = HostMessage(machine_msg=output)
    message_service.add_message(task_new, host_msg)

    # get latest task object
    task_final = task_service.get_task(task_new.taskId)

    return task_final
