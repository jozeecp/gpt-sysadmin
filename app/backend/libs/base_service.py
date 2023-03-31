"""base service"""

import os

# if unit testing, use fakeredis
if os.environ.get("TESTING") == "True":
    from fakeredis import FakeRedis as RedisInit
else:
    from redis import Redis as RedisInit

redis_user = os.environ.get("REDIS_USER")
redis_pw = os.environ.get("REDIS_PW")
redis_host = os.environ.get("REDIS_HOST")


class BaseService:
    """Base service"""

    def __init__(self, redis_db):
        self.redis_client = RedisInit(
            host=redis_host,
            port=6379,
            db=redis_db,
            username=redis_user,
            password=redis_pw,
        )
