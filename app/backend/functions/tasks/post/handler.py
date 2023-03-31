"""Task creation handler"""
from app.backend.libs.cmd_service import CmdService
from app.backend.libs.generative_cmd_service import GenerativeCmdService
from app.backend.libs.task_service import MessageService, TaskService
from app.backend.models.task import HostMessage, Task


def handler(task_old: Task) -> Task:
    """Handle task creation"""

    task_service = TaskService()
    message_service = MessageService()

    # create task
    task_new = task_service.create_task(task_old)
    print("task_old:", task_old)
    print("task_new:", task_new)

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
