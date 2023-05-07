"""Command service."""
import io
import os
from contextlib import contextmanager
from os.path import exists

import paramiko
from libs.base_service import BaseService
from libs.utils import LoggingService
from models.host import HostCreate
from models.task import Message, Task

logger = LoggingService.get_logger(__name__)

redis_db = os.environ.get("PARAMIKO_REDIS_DB")
password = os.environ.get("SSH_PASSWORD")


class CmdService(BaseService):
    """Command service."""

    def __init__(self, task: Task, redis_client=None):
        super().__init__(redis_db=redis_db)
        self.task = task
        self.redis_client = redis_client or self.redis_client

    def execute_command(self, command: Message) -> str:
        """Execute a command."""
        cmd = command.machine_msg
        with self.ssh_connection(self.task) as client:
            return self._exec_command(client, cmd)

    def _exec_command(self, client, command):
        """Execute a command."""
        try:
            _, stdout, stderr = client.exec_command(command)
        except paramiko.ssh_exception.SSHException as e:
            # Handle SSHException if needed
            logger.error("SSHException: %s", e)
            raise e

        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        return output or error

    @contextmanager
    def ssh_connection(self, task: Task):
        """Create an SSH connection."""

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with open("/root/.ssh/id_rsa", "r") as key_file:
            key_content = key_file.read()
            keyfile = io.StringIO(key_content)
            private_key = paramiko.RSAKey.from_private_key(keyfile)

        ssh_client.connect(
            hostname=task.host.hostname,
            username=task.host.username,
            pkey=private_key,
        )
        try:
            yield ssh_client
        finally:
            ssh_client.close()

    @staticmethod
    def ssh_connection_test(host: HostCreate) -> bool:
        """
        Test SSH connection

        Returns:
            bool: True if SSH connection is successful
        """

        assert exists("/root/.ssh/id_rsa"), "SSH key does not exist"
        logger.debug("SSH key exists")

        logger.debug("creating ssh client...")
        ssh_client = paramiko.SSHClient()
        logger.debug("ssh_client: %s", ssh_client.__dict__)

        logger.debug("setting missing host key policy...")
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with open("/root/.ssh/id_rsa", "r") as key_file:
            logger.debug("key_file: %s", key_file)
            private_key = paramiko.RSAKey.from_private_key(key_file)
            logger.debug("private_key: %s", private_key)

        try:
            logger.debug("Testing SSH connection with host: %s", host.hostname)
            ssh_client.connect(
                hostname=host.hostname,
                username=host.username,
                pkey=private_key,
            )
            logger.info("Successfully connected to host: %s", host.hostname)
        except paramiko.ssh_exception.AuthenticationException as e:
            logger.error("AuthenticationException: %s", e)
            return False
        except paramiko.ssh_exception.SSHException as e:
            logger.error("SSHException: %s", e)
            return False
        finally:
            ssh_client.close()

        return True

    @staticmethod
    def register_ssh_key(host: HostCreate) -> None:
        """
        Register SSH key
        """

        logger.debug("Registering SSH key...")

        assert host
