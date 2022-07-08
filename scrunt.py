from database import DataBase
from log import Log


class Scrunt:
    _STATUS_START: int = 1
    _STATUS_OK: int = 2
    _STATUS_CANCEL: int = 3
    _STATUS_ERROR: int = 4

    def __init__(self, run_id: int):
        self._run_id = run_id

        self._db = DataBase()

        self._log = Log(self._db, self._run_id)

    def log(self):
        return self._log

