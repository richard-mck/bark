"""Commands to execute for the business logic layer"""

from datetime import datetime

from database import DatabaseManager

db = DatabaseManager("bookmarks.db")


class CreateBookmarksTableCommand:
    """Create the DB table for storing the user's bookmarks"""

    def execute(self):
        db.create_table(
            "bookmarks",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "title": "TEXT NOT NULL",
                "url": "TEXT NOT NULL",
                "notes": "TEXT",
                "date_added": "TEXT NOT NULL",
            },
        )


class AddBookmarksCommand:
    """Given a new bookmark, add this to the table with the current date and time"""

    def execute(self, data: dict[str, str]) -> str:
        data["date_added"] = datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return f"Successfully added '{data['title']}' to bookmarks"


class ListBookmarksCommand:
    """List all bookmarks in the DB, optionally sorting on a specific column"""

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self) -> list:
        return db.select("bookmarks", None, self.order_by).fetchall()
