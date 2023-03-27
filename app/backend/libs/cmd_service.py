"""Command service."""
import os
import pickle

import paramiko
from app.backend.libs.base_service import BaseService
from app.backend.models.task import Task

redis_db = os.environ.get("PARAMIKO_REDIS_DB")

# FIXME: need better way to authenticate SSH via keys
password = os.environ.get("SSH_PASSWORD")


class CmdService(BaseService):
    """Command service."""

    def __init__(self, task: Task):
        super().__init__(redis_db=redis_db)
        self.task = task

    def execute_command(self, command: str) -> str:
        """
        Execute a command on a remote host.

        :param task_id: Request ID
        :param command: Command to execute

        :return: Output of command
        """
        # Retrieve serialized client from Redis using request ID as key
        # or use the following code to set up a new SSH client
        if self.redis_client.get(self.task.taskId) is None:
            client = self.refresh_client(self.task.taskId)
        else:
            client = self.retrieve_client(self.task.taskId)

        # Use client to execute command, catch stale connections exception
        try:
            _, stdout, stderr = client.exec_command(command)
        except paramiko.ssh_exception.SSHException:
            client = self.refresh_client(self.task.taskId)
            _, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        # Print output or do something else with it
        print(output)

        # store client in Redis
        self.store_client(self.task.taskId, client, close=True)

        # return output or error
        return output or error

    def store_client(self, task_id, client, close=False) -> None:
        """Store client in Redis."""
        client_bytes = pickle.dumps(client)
        if close:
            client.close()
        self.redis_client.set(task_id, client_bytes)

    def retrieve_client(self, task_id) -> paramiko.SSHClient:
        """Retrieve client from Redis."""
        client_bytes = self.redis_client.get(task_id)
        client = pickle.loads(client_bytes)
        return client

    def refresh_client(self, task: Task) -> paramiko.SSHClient:
        """Refresh client in Redis."""
        # start a new SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=task.host,
            username=task.user,
            password=password,
        )

        self.store_client(task.taskId, client)
        return client
