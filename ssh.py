from log import Log
import paramiko


class SSH:
    def __init__(self, log: Log, hostname: str, username: str, password: str):
        self._log = log
        self._hostname = hostname
        self._username = username
        self._stdin = None
        self._stdout = None
        self._stderr = None

        self._ssh = self._connect(hostname, username, password)

    def _connect(self, hostname: str, username: str, password: str):
        self._log.info("Initialize ssh on {}, username: {}".format(hostname, username))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)

        return ssh

    def exec(self, command: str):
        self._log.info("Execute command {} on {}, username: {}".format(command, self._hostname, self._username))

        self._stdin, self._stdout, self._stderr = self._ssh.exec_command('echo "Hello"')

    def get_std_out(self):
        return self._stdout

    def get_std_err(self):
        return self._stderr

    def close(self):
        self._log.info("Close ssh on {}, username: {}".format(self._hostname, self._username))
        self._ssh.close()
