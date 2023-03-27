from pydantic import BaseModel
from typing import List, Optional, Union


class Message(BaseModel):
    """Message model"""

    role: str = "user"


class GPTMessage(Message):
    """Message model"""

    role: str = "assistant"
    human_msg: str
    machine_msg: str


class HostMessage(Message):
    """Message model"""

    machine_msg: str


class SystemMessage(Message):
    """Message model"""

    role: str = "system"
    prompt: str


class Task(BaseModel):
    """Task model"""

    taskId: str
    status: str
    taskDescription: str
    hostDescription: str
    host: str
    user: str
    supervised: bool
    messages: List[Union[Message, GPTMessage, HostMessage, SystemMessage]] = []


class ParsedMessage(BaseModel):
    """Parsed message model"""

    role: str
    content: str
