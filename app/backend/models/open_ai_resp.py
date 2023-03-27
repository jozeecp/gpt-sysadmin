"""OpenAI response model"""

from typing import (
    List,
)

from pydantic import BaseModel
from app.backend.models.task import Message


class Usage(BaseModel):
    """Usage model"""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @property
    def cost(self) -> float:
        """Get cost of usage"""
        # 	$0.03 / 1K tokens
        cost = self.total_tokens * 0.00003
        return cost


class OpenAIMessage(BaseModel):
    """OpenAI message model"""

    role: str
    content: str


class Choice(BaseModel):
    """Choice model"""

    message: OpenAIMessage
    index: int
    finish_reason: str


class OpenAIResponse(BaseModel):
    """OpenAI response model"""

    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]
