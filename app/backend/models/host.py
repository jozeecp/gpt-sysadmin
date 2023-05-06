"""Host model"""
from typing import Optional

from pydantic import BaseModel


class HostBase(BaseModel):
    """Base host model"""


    host_id: str
    hostname: str
    description: str
    ip: Optional[str]
    username: str = "root"


class HostCreate(HostBase):
    """Host creation model"""

    password: Optional[str]


class Host(HostBase):
    """Host model"""
