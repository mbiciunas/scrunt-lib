from .database import DataBase
import logging
from .log_handler import LogHandler


class Log:
    _LOG_DEBUG: int = 10
    _LOG_INFO: int = 20
    _LOG_WARN: int = 30
    _LOG_ERROR: int = 40

    def __init__(self, database: DataBase, run_id: int):
        self._database = database
        self._run_id = run_id

        self._logger = logging.getLogger("MyLogger")
        handler = LogHandler(self._database, self._run_id)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)
        self.info("Initialized logging")

    def debug(self, debug: str):
        self._logger.debug(debug)

    def info(self, info: str):
        self._logger.info(info)

    def warning(self, warning: str):
        self._logger.warning(warning)

    def error(self, value: str, trace: bool = False):
        if trace:
            self._logger.error(value, exc_info=True)
        else:
            self._logger.error(value, exc_info=False)
