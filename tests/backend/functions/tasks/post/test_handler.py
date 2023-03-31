"""Test handler function"""

import unittest
from unittest.mock import MagicMock

import openai

from app.backend.functions.tasks.post.handler import handler
from app.backend.models.task import HostMessage, Task


class TestHandler(unittest.TestCase):
    """Test handler function"""

    def test_handler(self):
        """Test handler function"""
        # Mock TaskService
        task_service = MagicMock()
        task_service.create_task.return_value = MagicMock()
        task_service.get_task.return_value = MagicMock()

        # Mock MessageService
        message_service = MagicMock()

        # Mock GenerativeCmdService
        generative_cmd_service = MagicMock()
        generative_cmd_service.generate_cmd.return_value = "sample command"

        # Mock CmdService
        cmd_service = MagicMock()
        cmd_service.execute_command.return_value = "sample output"

        # Mock Task
        task = MagicMock()
        task.taskId = "some_task_id"
        task.json.return_value = '{"key": "value"}'  # A valid JSON string

        # Mock OpenAI
        chat_completion_response = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": '{\
                            "human_msg": "sample command",\
                            "machine_msg": "sample output"\
                        }',
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
        }

        with unittest.mock.patch.object(
            openai.ChatCompletion, "create", return_value=chat_completion_response
        ), unittest.mock.patch(
            "app.backend.libs.task_service.TaskService", return_value=task_service
        ), unittest.mock.patch(
            "app.backend.libs.task_service.MessageService", return_value=message_service
        ), unittest.mock.patch(
            "app.backend.libs.generative_cmd_service.GenerativeCmdService",
            return_value=generative_cmd_service,
        ), unittest.mock.patch(
            "app.backend.libs.cmd_service.CmdService", return_value=cmd_service
        ):
            result = handler(task)

            # Verify task creation
            task_service.create_task.assert_called_once_with(task)

            # Verify command generation
            generative_cmd_service.generate_cmd.assert_called_once_with(task)

            # Verify adding gpt message
            message_service.add_message.assert_any_call(task, "sample command")

            # Verify command execution
            cmd_service.execute_command.assert_called_once_with("sample command")

            # Verify adding host message
            message_service.add_message.assert_any_call(
                task, HostMessage(machine_msg="sample output")
            )

            # Verify getting the latest task object
            task_service.get_task.assert_called_once_with(task.taskId)

            self.assertIsInstance(result, Task)


if __name__ == "__main__":
    unittest.main()
