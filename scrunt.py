from database import DataBase
from log import Log
from ssh import SSH


class Scrunt:
    _STATUS_START: int = 1
    _STATUS_OK: int = 2
    _STATUS_CANCEL: int = 3
    _STATUS_ERROR: int = 4

    def __init__(self, run_id: int):
        self._run_id = run_id

        self._db = DataBase()

        self._log = Log(self._db, self._run_id)

        self._ssh = SSH(self._log, "localhost", "mbiciunas", "M@rk8478")

    def log(self):
        return self._log

    def ssh(self):
        return self._ssh
