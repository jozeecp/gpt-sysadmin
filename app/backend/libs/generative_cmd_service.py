"""
Generative command service.

This service is responsible for generating commands based on the current state of the task.
Utilizes the OpenAI API to generate commands.
"""

import ast
import json
import os
from json.decoder import JSONDecodeError
from typing import Any, Dict, List

import openai
from libs.base_service import BaseService
from libs.task_service import MessageService
from libs.utils import LoggingService
from models.open_ai_resp import OpenAIResponse
from models.task import GPTMessage, ParsedMessage, Task

logger = LoggingService.get_logger(__name__)

# OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")

# redis db
redis_db = os.environ.get("TASK_REDIS_DB")


class GenerativeCmdService(BaseService):
    """Generative command service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def generate_cmd(self, task: Task) -> GPTMessage:
        """Generate a command"""

        logger.debug("In generate_cmd()...")
        # parse message list
        message_list = self.parse_message_list(task)
        logger.debug("message_list: %s", message_list)

        # use openai library to generate command
        logger.debug("Generating command...")
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=task.engine,
            messages=message_list,
            temperature=0,
        )
        logger.debug("OpenAI response: %s", response)

        gpt_msg = self.parse_openai_response(response)
        logger.debug("gpt_msg: %s", gpt_msg)

        return gpt_msg

    @staticmethod
    def parse_openai_response(response: Dict[str, Any]) -> GPTMessage:
        """Parse OpenAI response"""

        # response DTO
        response_obj = OpenAIResponse(**response)

        content = response_obj.choices[0].message.content

        try:
            # Try to load JSON string as dictionary
            content_dict = json.loads(content)
        except JSONDecodeError:
            # If single-quoted, convert JSON string to dictionary
            content_dict = ast.literal_eval(content)

        gpt_msg = GPTMessage(**content_dict)

        return gpt_msg

    @staticmethod
    def get_prompt(task: Task) -> str:
        """Get prompt for generating command"""

        # get last system message
        last_system_msg = task.messages[-1]

        # get prompt
        prompt = last_system_msg.prompt

        return prompt

    @staticmethod
    def parse_message_list(task: Task) -> List[Dict[str, Any]]:
        """Parse message list"""

        # get message list
        message_list = task.messages

        parsed_msg_list: List[ParsedMessage] = []
        for msg in message_list:
            # parse message
            parsed_msg = MessageService.parse_message(msg)
            parsed_msg_list.append(parsed_msg)

        api_ready_msg_list = []
        for msg in parsed_msg_list:
            api_ready_msg = {
                "role": msg.role,
                "content": msg.content,
            }
            api_ready_msg_list.append(api_ready_msg)

        return api_ready_msg_list
