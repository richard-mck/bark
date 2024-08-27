"""Managing the persistence layer for Bark"""

import pathlib
import sqlite3


class DatabaseManager:
    def __init__(self, db_filename: pathlib.Path):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values=None) -> sqlite3.Cursor:
        """Given an SQL statement and values, execute it, returning the cursor containing the result"""
        with self.connection:
            # Using `with` here ensures execution occurs as a transaction
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: dict[str, str]):
        """Given a table name and a dict in the form `{$TYPE: $NAME}`, create a new table"""
        columns_with_types = [
            f"{column_name} {column_type}"
            for column_name, column_type in columns.items()
        ]
        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

    def add(self, table_name: str, data: dict[str, str]):
        """Given a table name and a dict in the form `{$TYPE: $NAME}`, add this data into the table"""
        placeholder_str = ", ".join("?" * len(data))
        data_names = ", ".join(data.keys())
        data_values = tuple(data.values())
        self._execute(
            f"""
            INSERT INTO {table_name}
            ({data_names})
            VALUES ({placeholder_str})
            """,
            data_values,
        )

    def delete(self, table_name: str, data: dict[str, str]):
        """Given a table name and a dict in the form `{$TYPE: $NAME}`, remove this data from the table"""
        placeholder_str = [f"{data_name} = ?" for data_name in data.keys()]
        delete_criteria = " AND ".join(placeholder_str)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria}
            """,
            tuple(data.values()),
        )

    def select(self, table_name: str, criteria=None, order_by=None) -> sqlite3.Cursor:
        """
        Search a given table for matching data
        :param table_name: table to search within
        :param criteria: optional dict in the form `{$TYPE: $NAME}`, columns to search and the values to search for
        :param order_by: optional column to sort on
        :return: SQLite Cursor
        """
        criteria = criteria or {}
        query = f"SELECT * FROM {table_name}"
        if criteria:
            placeholder_str = [
                f"{criteria_name} = ?" for criteria_name in criteria.keys()
            ]
            select_criteria = " AND ".join(placeholder_str)
            query += f" WHERE {select_criteria}"
        order_placeholder = f" ORDER BY {order_by}" if order_by else ""
        return self._execute(
            query + order_placeholder,
            tuple(criteria.values()),
        )
