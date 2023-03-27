"""parser factory"""
from typing import Union

from app.backend.models.task import (
    GPTMessage,
    HostMessage,
    Message,
    SystemMessage,
    ParsedMessage,
)


class ParserFactory:
    """Parser factory"""

    @staticmethod
    def get_parser(msg: Message):
        """Get a parser"""
        if isinstance(msg, GPTMessage):
            return GPTParser()
        if isinstance(msg, SystemMessage):
            return SystemParser()
        if isinstance(msg, HostMessage):
            return HostParser()


class GPTParser:
    """GPT parser"""

    def parse(self, msg: GPTMessage) -> ParsedMessage:
        """Parse a GPT message"""
        content = {
            "human_msg": msg.human_msg,
            "machine_msg": msg.machine_msg,
        }

        content_str = str(content)

        return ParsedMessage(role=msg.role, content=content_str)


class SystemParser:
    """System parser"""

    def parse(self, msg: SystemMessage) -> ParsedMessage:
        """Parse a system message"""
        content = msg.prompt

        content_str = content

        return ParsedMessage(role=msg.role, content=content_str)


class HostParser:
    """Host parser"""

    def parse(self, msg: HostMessage) -> ParsedMessage:
        """Parse a host message"""
        content = msg.machine_msg

        content_str = content

        return ParsedMessage(role=msg.role, content=content_str)
