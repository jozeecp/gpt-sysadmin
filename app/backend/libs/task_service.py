"""Task service"""
import os

# import jinja2
from app.backend.libs.base_service import BaseService
from app.backend.libs.parser_factory import ParserFactory
from app.backend.models.task import Message, ParsedMessage
from app.backend.models.task import (
    Task,
    SystemMessage,
)
from jinja2 import Template

redis_db = os.environ.get("TASK_REDIS_DB")


class MessageSerivce(BaseService):
    """Message service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def add_message(self, task: Task, message: Message):
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

    def create_task(self, task: Task) -> None:
        """Create a new task"""

        # render jinja2 template to get prompt
        with open("templates/prompt.jinja2", "r") as f:
            template = Template(f.read())
            f.close()
        prompt = template.render(task=task.dict())

        # initialize first message
        task.messages.append(SystemMessage(prompt=prompt))

        # register task in redis
        self.redis_client.set(task.taskId, task.json())

        return
