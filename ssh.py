from log import Log
import paramiko
import select


class SSH:
    def __init__(self, log: Log, hostname: str, username: str, password: str):
        self._log = log
        self._hostname = hostname
        self._username = username
        self._stdin = None
        self._stdout = None
        self._stderr = None
        self._status = None

        self._ssh = self._connect(hostname, username, password)

    def _connect(self, hostname: str, username: str, password: str):
        self._log.info("Initialize ssh on {}, username: {}".format(hostname, username))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)

        return ssh

    def exec(self, command: str, timeout: int = 5):
        # one channel per command
        self._log.info("execute command: {}".format(command))
        stdin, stdout, stderr = self._ssh.exec_command(command)
        # get the shared channel for stdout/stderr/stdin
        self._log.debug("Get standard out channel")
        channel = stdout.channel

        # we do not need stdin.
        self._log.debug("Close stdin")
        stdin.close()
        # indicate that we're not going to write to that channel anymore
        self._log.debug("Shutdown write to standard out channel")
        channel.shutdown_write()

        # read stdout/stderr in order to prevent read block hangs
        stdout_chunks = []
        stdout_chunks.append(stdout.channel.recv(len(stdout.channel.in_buffer)).decode())
        # chunked read to prevent stalls
        while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
            self._log.debug("Loop while waiting for channel")
            # stop if channel was closed prematurely, and there is no data in the buffers.
            got_chunk = False
            readq, _, _ = select.select([stdout.channel], [], [], timeout)
            for c in readq:
                if c.recv_ready():
                    self._log.debug("Receive ready on standard out: {}".format(c.recv_ready()))
                    stdout_chunks.append(stdout.channel.recv(len(c.in_buffer)).decode())
                    got_chunk = True
                if c.recv_stderr_ready():
                    self._log.debug("Receive ready on standard out: {}".format(c.recv_stderr_ready()))
                    stderr.channel.recv_stderr(len(c.in_stderr_buffer))
                    got_chunk = True

            if not got_chunk \
                    and stdout.channel.exit_status_ready() \
                    and not stderr.channel.recv_stderr_ready() \
                    and not stdout.channel.recv_ready():
                self._log.debug("Done reading")
                stdout.channel.shutdown_read()
                # close the channel
                stdout.channel.close()
                break  # exit as remote side is finished and our bufferes are empty

        self._log.debug("Done loop, close stdout, stderr")
        # close all the pseudofiles
        stdout.close()
        stderr.close()

        self._status = stdout.channel.recv_exit_status()
        self._stdout = ''.join(stdout_chunks)

    # def exec(self, command: str):
    #     self._log.info("Execute command {} on {}, username: {}".format(command, self._hostname, self._username))
    #
    #     self._stdin, self._stdout, self._stderr = self._ssh.exec_command(command)

    def get_std_out(self):
        return self._stdout

    def get_std_err(self):
        return self._stderr

    def get_status(self):
        return self._status

    def close(self):
        self._log.info("Close ssh on {}, username: {}".format(self._hostname, self._username))
        self._ssh.close()
        self._ssh = None
        self._stdin = None
        self._stdout = None
        self._stderr = None
