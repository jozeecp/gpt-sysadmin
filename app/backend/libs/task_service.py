"""Task service"""
import json
import os

from jinja2 import Template

# import jinja2
from libs.base_service import BaseService
from libs.host_service import HostService
from libs.parser_factory import ParserFactory
from libs.utils import LoggingService
from models.task import Message, ParsedMessage, SystemMessage, Task

redis_db = os.environ.get("TASK_REDIS_DB")

logger = LoggingService.get_logger(__name__)


class MessageService(BaseService):
    """Message service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def add_message(self, task: Task, message: Message) -> Task:
        """Add a message to a task"""

        logger.debug("In add_message()...")

        # parse message
        parsed_msg = self.parse_message(message)
        logger.debug("parsed_msg: %s", parsed_msg)

        # add message to task
        task.messages.append(message)
        logger.debug("task: %s", task)

        # update task in redis
        task_json = json.dumps(task.dict())
        logger.debug("task_json: %s", task_json)
        self.redis_client.set(task.taskId, task_json)

        logger.debug("returning from add_message()")
        return task

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

        # logger.debug("returning early from task service")
        # return task

        # add host to task
        logger.debug("adding host to task")
        host_service = HostService()
        host = host_service.get_host(task.host_id)
        task.host = host
        logger.debug(f"task.host: {task.host}")

        # render jinja2 template to get system prompt
        logger.debug("rendering jinja2 template to get system prompt")
        with open("./templates/sys_prompt.jinja2", encoding="utf-8") as f:
            template = Template(f.read())
            f.close()
        sys_prompt = template.render(task=task.dict())
        logger.debug(f"sys_prompt: {sys_prompt}")

        # add first message (system prompt)
        logger.debug("adding first message (system prompt)")
        task.messages.append(SystemMessage(prompt=sys_prompt))
        logger.debug(f"task.messages: {task.messages}")

        # register task in redis
        self.redis_client.set(task.taskId, task.json())

        return task

    def get_task(self, task_id: str) -> Task:
        """Get a task"""

        # get task from redis
        task_json = self.redis_client.get(task_id)
        logger.debug(f"task_json[get_task()]: {str(task_json)}")
        task_dict = json.loads(task_json)
        logger.debug(f"task_dict[get_task()]: {task_dict}")
        task = Task(**task_dict)
        logger.debug(f"task[get_task()]: {task}")

        return task

    def update_task(self, task: Task) -> Task:
        """Update a task"""

        # update task in redis
        task_json = json.dumps(task.dict())
        logger.debug(f"task_json[update_task()]: {task_json}")
        self.redis_client.set(task.taskId, task_json)

        return task
