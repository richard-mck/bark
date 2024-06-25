"""Managing the persistence layer for Bark"""
import pathlib
import sqlite3


class DatabaseManager:
    def __init__(self, db_filename: pathlib.Path):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values=None):
        """Given an SQL statement and values, execute it, returning the cursor containing the result"""
        with self.connection:
            # Using `with` here ensures execution occurs as a transaction
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor
