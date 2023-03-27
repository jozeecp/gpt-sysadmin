"""Command service."""
import os
import pickle

import paramiko
from backend.libs.base_service import BaseService

redis_db = os.environ.get("PARAMIKO_REDIS_DB")


class CmdService(BaseService):
    """Command service."""

    def __init__(self):
        super().__init__(redis_db=redis_db)

    def execute_command(self, request_id, command) -> str:
        """
        Execute a command on a remote host.

        :param request_id: Request ID
        :param command: Command to execute

        :return: Output of command
        """
        # Retrieve serialized client from Redis using request ID as key
        # or use the following code to set up a new SSH client
        if self.redis_client.get(request_id) is None:
            client = self.refresh_client(request_id)
        else:
            client = self.retrieve_client(request_id)

        # Use client to execute command, catch stale connections exception
        try:
            _, stdout, stderr = client.exec_command(command)
        except paramiko.ssh_exception.SSHException:
            client = self.refresh_client(request_id)
            _, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        # Print output or do something else with it
        print(output)

        # store client in Redis
        self.store_client(request_id, client, close=True)

        # return output or error
        return output or error

    def store_client(self, request_id, client, close=False) -> None:
        """Store client in Redis."""
        client_bytes = pickle.dumps(client)
        if close:
            client.close()
        self.redis_client.set(request_id, client_bytes)

    def retrieve_client(self, request_id) -> paramiko.SSHClient:
        """Retrieve client from Redis."""
        client_bytes = self.redis_client.get(request_id)
        client = pickle.loads(client_bytes)
        return client

    def refresh_client(self, request_id) -> paramiko.SSHClient:
        """Refresh client in Redis."""
        # start a new SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname="your_server_hostname",
            username="your_username",
            password="your_password",
        )

        self.store_client(request_id, client)
        return client
