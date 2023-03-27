from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


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


class ParsedMessage(BaseModel):
    """Parsed message model"""

    role: str
    content: str


class EngineEnum(str, Enum):
    """Engine enum"""

    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class StatusEnum(str, Enum):
    """Status enum"""

    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """Task model"""

    taskId: str
    engine: EngineEnum
    status: StatusEnum
    taskDescription: str
    hostDescription: str
    host: str
    user: str
    supervised: bool
    messages: List[Message] = []
    parsedMessages: List[ParsedMessage] = []
