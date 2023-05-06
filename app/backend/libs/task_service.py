"""Task service"""
import os

from jinja2 import Template

# import jinja2
from libs.base_service import BaseService
from libs.host_service import HostService
from libs.parser_factory import ParserFactory
from models.task import Message, ParsedMessage, SystemMessage, Task

redis_db = os.environ.get("TASK_REDIS_DB")


class MessageService(BaseService):
    """Message service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def add_message(self, task: Task, message: Message) -> Task:
        """Add a message to a task"""

        # parse message
        parsed_msg = self.parse_message(message)

        # add message to task
        task.messages.append(message)

        # update task in redis
        self.redis_client.set(task.taskId, task.json())

        return parsed_msg

    @staticmethod
    def parse_message(message: Message) -> ParsedMessage:
        """Parse a message"""

        # parser factory
        parser = ParserFactory.get_parser(message)
        parsed_msg = parser.parse(message)

        return parsed_msg


class TaskService(BaseService):
    """Task service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def create_task(self, task: Task) -> Task:
        """Create a new task"""

        # render jinja2 template to get system prompt
        with open("./templates/sys_prompt.jinja2", encoding="utf-8") as f:
            template = Template(f.read())
            f.close()
        sys_prompt = template.render(task=task.dict())

        # add first message (system prompt)
        task.messages.append(SystemMessage(prompt=sys_prompt))

        # add host to task
        host_service = HostService()
        host = host_service.get_host(task.hostId)
        task.host = host

        # register task in redis
        self.redis_client.set(task.taskId, task.json())

        return task

    def get_task(self, task_id: str) -> Task:
        """Get a task"""

        # get task from redis
        task_json = self.redis_client.get(task_id)
        task = Task(**task_json)

        return task
