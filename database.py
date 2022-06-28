import sqlite3


class DataBase:
    def __init__(self):
        self._connection = sqlite3.connect("/home/mbiciunas/go/src/scrunt-back/.scrunt/database/runtime.db")
        self._cursor = self._connection.cursor()

    def insert_runs(self, script_id, status):
        self._cursor.execute("INSERT INTO runs (script_id, status) VALUES (?, ?)", (script_id, status))
        self._connection.commit()

        return self._cursor.lastrowid

    def insert_outputs(self, run_id, output_type, value):
        self._cursor.execute("INSERT INTO outputs (run_id, type, value) VALUES (?, ?, ?)", (run_id, output_type, value))
        self._connection.commit()

        return self._cursor.lastrowid

    def close(self):
        if self._cursor:
            self._cursor.close()

        if self._connection:
            self._connection.close()

