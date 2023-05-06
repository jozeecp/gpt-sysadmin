"""Secrets service"""
import os

from libs.base_service import BaseService

redis_db = os.environ.get("SECRETS_REDIS_DB")


class SecretsService(BaseService):
    """Secrets service"""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def set_secret(self, secret_id: str, secret: str) -> str:
        """Set secret in redis"""

        # set secret in redis
        self.redis_client.set(secret_id, secret)

        return secret_id

    def get_secret(self, secret_id: str) -> str:
        """Get secret from redis"""

        # get secret from redis
        secret = self.redis_client.get(secret_id)

        return secret
