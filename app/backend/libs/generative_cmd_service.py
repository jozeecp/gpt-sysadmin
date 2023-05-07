"""
Generative command service.

This service is responsible for generating commands based on the current state of the task.
Utilizes the OpenAI API to generate commands.
"""

import json
import os
from typing import Any, Dict, List

import openai
from libs.base_service import BaseService
from libs.task_service import MessageService
from models.open_ai_resp import OpenAIResponse
from models.task import GPTMessage, ParsedMessage, Task

# OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")

# redis db
redis_db = os.environ.get("TASK_REDIS_DB")


class GenerativeCmdService(BaseService):
    """Generative command service
    FIXME: This is a stub. It needs to be implemented."""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def generate_cmd(self, task: Task) -> GPTMessage:
        """Generate a command"""

        # parse message list
        message_list = self.parse_message_list(task)

        # use openai library to generate command
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=task.engine,
            messages=message_list,
            temperature=0,
            # max_tokens=8000,
        )

        gpt_msg = self.parse_openai_response(response)

        return gpt_msg

    @staticmethod
    def parse_openai_response(response: Dict[str, Any]) -> GPTMessage:
        """Parse OpenAI response"""

        # response DTO
        response_obj = OpenAIResponse(**response)

        content = response_obj.choices[0].message.content
        content_dict = json.loads(content)

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
