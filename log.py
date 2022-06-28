from database import DataBase


class Log:
    _LOG_DEBUG: int = 1
    _LOG_INFO: int = 2
    _LOG_WARN: int = 3
    _LOG_ERROR: int = 4

    def __init__(self, database: DataBase, run_id: int):
        self._database = database
        self._run_id = run_id
        self.info("Initialize logging")

    def debug(self, debug: str):
        self._insert(Log._LOG_DEBUG, debug)

    def info(self, info: str):
        self._insert(Log._LOG_INFO, info)

    def warning(self, warning: str):
        self._insert(Log._LOG_WARN, warning)

    def error(self, error: str):
        self._insert(Log._LOG_ERROR, error)

    def _insert(self, log_type: int, value: str):
        self._database.insert_outputs(self._run_id, log_type, value)

