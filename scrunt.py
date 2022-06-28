from database import DataBase
from log import Log


class Scrunt:
    _STATUS_START: int = 1
    _STATUS_OK: int = 2
    _STATUS_CANCEL: int = 3
    _STATUS_ERROR: int = 4

    def __init__(self, script_id: int):
        self._script_id = script_id

        self._init_db()
        self._init_log()

    def _init_db(self):
        self._db = DataBase()

        self._run_id = self._db.insert_runs(self._script_id, Scrunt._STATUS_START)

    def _init_log(self):
        self._log = Log(self._db, self._run_id)

        self._log.info("Initialize logging")

    def log(self):
        return self._log


if __name__ == '__main__':
    scrunt = Scrunt(1)

    scrunt.log().info("This is a new info entry")
