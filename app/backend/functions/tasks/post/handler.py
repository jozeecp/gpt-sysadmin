"""Task creation handler"""
from backend.libs.cmd_service import CmdService
from backend.libs.generative_cmd_service import GenerativeCmdService
from backend.libs.task_service import MessageService, TaskService
from backend.models.task import HostMessage, Task


def handler(task: Task) -> Task:
    """Handle task creation"""

    task_service = TaskService()
    message_service = MessageService()

    # create task
    task = task_service.create_task(task)

    # generate command
    cmd = GenerativeCmdService().generate_cmd(task)

    # add gpt message
    message_service.add_message(task, cmd)

    # run command
    cmd_service = CmdService(task)
    output = cmd_service.execute_command(cmd)

    # add host message
    host_msg = HostMessage(machine_msg=output)
    message_service.add_message(task, host_msg)

    # get latest task object
    task = task_service.get_task(task.taskId)

    return Task
