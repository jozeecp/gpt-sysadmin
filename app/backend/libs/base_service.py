"""base service"""

import os

import redis

redis_user = os.environ.get("REDIS_USER")
redis_pw = os.environ.get("REDIS_PW")
redis_host = os.environ.get("REDIS_HOST")

class BaseService:
    """Base service"""
    def __init__(self, redis_db):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=6379,
            db=redis_db,
            username=redis_user,
            password=redis_pw,
        )
