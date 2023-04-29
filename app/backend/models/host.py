from pydantic import BaseModel


class Host(BaseModel):
    """Host model"""

    host_id: str
    host_name: str
    ip: str

    username: str
    private_key: str
    public_key: str
