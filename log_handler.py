from .database import DataBase
import sqlite3
import logging


class LogHandler(logging.Handler):
    def __init__(self, database: DataBase, run_id: int):
        self._database = database
        self._run_id = run_id

        logging.Handler.__init__(self)

    def emit(self, record):
        """
        Connect to DB, execute SQL Request, disconnect from DB
        @param record:
        @return:
        """
        # Use default formatting:
        self.format(record)

        # Replace single quotes in messages
        if isinstance(record.__dict__['message'], str):
            record.__dict__['message'] = record.__dict__['message'].replace("'", "''")

        if isinstance(record.__dict__['msg'], str):
            record.__dict__['msg'] = record.__dict__['msg'].replace("'", "''")

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)

            # Insert log record:
            self._insert(record.levelno,
                         "{}\n {} |3|{} |4|{} |5|{} |6|{} |7|{} |8|{}".format(record.msg,
                                                                              record.exc_text,
                                                                              record.filename,
                                                                              record.funcName,
                                                                              record.lineno,
                                                                              record.module,
                                                                              record.levelname,
                                                                              record.stack_info))
        else:
            record.exc_text = ""

            # Insert log record:
            self._insert(record.levelno, record.msg)

    def _insert(self, log_type: int, value: str):
        connection = sqlite3.connect("/home/mbiciunas/go/src/scrunt-back/.scrunt/database/runtime.db")
        connection.execute("INSERT INTO outputs (run_id, type, value) VALUES (?, ?, ?)", (self._run_id, log_type, str(value)))
        connection.commit()
