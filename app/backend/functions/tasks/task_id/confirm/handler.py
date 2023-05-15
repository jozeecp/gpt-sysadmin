from models.task import Task, GPTMessage, HostMessage
from libs.task_service import TaskService, MessageService
from libs.generative_cmd_service import GenerativeCmdService
from libs.cmd_service import CmdService
from libs.utils import LoggingService

logger = LoggingService.get_logger(__name__)

def handler(task_id: str) -> Task:
    """
    Continues to the next step in a task.
    """

    # get task
    task_service = TaskService()
    task = task_service.get_task(task_id)
    logger.info("Task: %s", task)

    # run command
    cmd_service = CmdService(task)
    latest_cmd: GPTMessage = task.messages[-1]
    logger.info("Latest command: %s", latest_cmd)
    output: HostMessage = cmd_service.execute_command(latest_cmd)
    logger.info("Output: %s", output)

    # add message from host
    message_service = MessageService()
    task = message_service.add_message(task, output)

    # generate next command
    generative_cmd_service = GenerativeCmdService()
    gpt_msg = generative_cmd_service.generate_cmd(task)
    task = message_service.add_message(task, gpt_msg)

    # return task
    return task
