"""base service"""

import os

# if unit testing, use fakeredis
if os.environ.get("TESTING") == "True":
    from fakeredis import FakeRedis as RedisInit
else:
    from redis import Redis as RedisInit

# Remove the redis_user variable, as Redis versions prior to 6.0 do not use usernames
redis_pw = os.environ.get("REDIS_PW")
redis_host = os.environ.get("REDIS_HOST")


class BaseService:
    """Base service"""

    def __init__(self, redis_db):
        # Remove the username parameter when creating the Redis connection
        self.redis_client = RedisInit(
            host=redis_host,
            port=6379,
            db=redis_db,
            password=redis_pw,
        )
