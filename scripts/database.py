import sqlite3


class DataBase:
    def __init__(self):
        self._connection = sqlite3.connect("/home/mbiciunas/go/src/scrunt-back/.scrunt/database/runtime.db")
        # self._cursor = self._connection.cursor()

    def insert_runs(self, script_id, status):
        _cursor = self._connection.cursor()
        _cursor.execute("INSERT INTO runs (script_id, status) VALUES (?, ?)", (script_id, status))
        self._connection.commit()
        _cursor.close()
        # print("insert_runs - _cursor.lastrowid:",  _cursor.lastrowid)

        return _cursor.lastrowid

    def insert_outputs(self, run_id: int, output_type: int, value, split: bool = True):
        _cursor = self._connection.cursor()
        if isinstance(value, str) and split:
            for _line in value.splitlines():
                # print("insert_outputs - _line:", _line)
                _cursor.execute("INSERT INTO outputs (run_id, type, value) VALUES (?, ?, ?)", (run_id, output_type, _line))
        else:
            # print("insert_outputs - value:", value)
            _cursor.execute("INSERT INTO outputs (run_id, type, value) VALUES (?, ?, ?)", (run_id, output_type, str(value)))

        self._connection.commit()
        _cursor.close()
        # print("insert_outputs - _cursor.lastrowid:",  _cursor.lastrowid)

        return _cursor.lastrowid

    def close(self):
        # if self._cursor:
        #     self._cursor.close()

        if self._connection:
            self._connection.close()
