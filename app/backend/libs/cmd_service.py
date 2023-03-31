"""Command service."""
import os
import pickle
from contextlib import contextmanager
from unittest.mock import MagicMock

import paramiko

from app.backend.libs.base_service import BaseService
from app.backend.models.task import Task

redis_db = os.environ.get("PARAMIKO_REDIS_DB")
password = os.environ.get("SSH_PASSWORD")


class CmdService(BaseService):
    """Command service."""

    def __init__(self, task: Task, redis_client=None, ssh_client=None):
        super().__init__(redis_db=redis_db)
        self.task = task
        self.redis_client = redis_client or self.redis_client
        self.ssh_client = ssh_client or self.create_ssh_client()

    def create_ssh_client(self):
        """Create an SSH client."""
        if os.environ.get("TESTING") == "True":
            ssh_client = MagicMock()
            ssh_client.exec_command.return_value = (None, MagicMock(), MagicMock())
            ssh_client.exec_command.return_value[1].read.return_value = b"Sample output"
            ssh_client.exec_command.return_value[2].read.return_value = b""
            return ssh_client
        return None

    @contextmanager
    def ssh_connection(self, task: Task):
        """Create an SSH connection."""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                hostname=task.host,
                username=task.user,
                password=password,
            )
        try:
            yield self.ssh_client
        finally:
            self.ssh_client.close()
            self.ssh_client = None

    def execute_command(self, command: str) -> str:
        """Execute a command."""
        if self.redis_client.get(self.task.taskId) is None:
            with self.ssh_connection(self.task) as client:
                return self._exec_command(client, command)
        else:
            client = self.retrieve_client(self.task.taskId)
            return self._exec_command(client, command)

    def _exec_command(self, client, command):
        """Execute a command."""
        try:
            _, stdout, stderr = client.exec_command(command)
        except paramiko.ssh_exception.SSHException:
            client = self.refresh_client(self.task)
            _, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        print(output)

        self.store_client(self.task.taskId, client, close=True)

        return output or error

    def store_client(self, task_id, client, close=False) -> None:
        """Store a client in Redis."""
        if os.environ.get("TESTING") == "True":
            return

        client_bytes = pickle.dumps(client)
        if close:
            client.close()
        self.redis_client.set(task_id, client_bytes)

    def retrieve_client(self, task_id) -> paramiko.SSHClient:
        """Retrieve a client from Redis."""
        client_bytes = self.redis_client.get(task_id)
        client = pickle.loads(client_bytes)
        return client

    def refresh_client(self, task: Task) -> paramiko.SSHClient:
        """Refresh a client."""
        with self.ssh_connection(task) as client:
            self.store_client(task.taskId, client)
            return client
