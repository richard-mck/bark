"""Managing persistence across different implementations"""

from abc import ABC, abstractmethod

from database import DatabaseManager


class PersistenceLayer(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by):
        raise NotImplementedError

    @abstractmethod
    def edit(self, bookmark_id, data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError


class BookmarksDatabase(PersistenceLayer):
    def __init__(self):
        """Create the DB table for storing the user's bookmarks"""
        self.table_name = "bookmarks"
        self.db = DatabaseManager("bookmarks.db")
        self.db.create_table(
            self.table_name,
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "title": "TEXT NOT NULL",
                "url": "TEXT NOT NULL",
                "notes": "TEXT",
                "date_added": "TEXT NOT NULL",
            },
        )

    def create(self, data):
        self.db.add(self.table_name, data)

    def list(self, order_by):
        return self.db.select(self.table_name, None, order_by).fetchall()

    def edit(self, bookmark_id, data):
        self.db.update(self.table_name, data["update"], {"id": bookmark_id})

    def delete(self, bookmark_id):
        self.db.delete(self.table_name, {"id": bookmark_id})
