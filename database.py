"""Managing the persistence layer for Bark"""
import pathlib
import sqlite3


class DatabaseManager:
    def __init__(self, db_filename: pathlib.Path):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()
