"""Commands to execute for the business logic layer"""

import sys
import requests
from abc import ABC, abstractmethod
from datetime import datetime

import persistence

bookmarks_db = persistence.BookmarksDatabase()


class Command(ABC):
    """An abstract base class to ensure all subsequent commands meet interface requirements"""

    @abstractmethod
    def execute(self, data):
        raise NotImplementedError


class AddBookmarksCommand(Command):
    """Given a new bookmark, add this to the table with the current date and time"""

    @staticmethod
    def execute(data: dict[str, str], timestamp=None) -> (bool, None):
        data["date_added"] = timestamp or datetime.utcnow().isoformat()
        bookmarks_db.create(data)
        return True, None


class ImportGitHubStarsCommand(Command):
    """Given a GitHub username, import their starred repos as bookmarks"""

    @staticmethod
    def _parse_bookmark_info(repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data: dict[str, str]) -> (bool, None):
        repos_imported = 0
        github_username = data["github_username"]
        keep_timestamps = data["keep_timestamps"]
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        while next_page_of_results:
            response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            for star in response.json():
                timestamp = datetime.strptime(star["starred_at"], "%Y-%m-%dT%H:%M:%SZ") if keep_timestamps else None
                AddBookmarksCommand.execute(self._parse_bookmark_info(star["repo"]), timestamp=timestamp)
                repos_imported += 1
            # Grab the Link header if present, otherwise an empty dict
            next_page_of_results = response.links.get("next", {}).get("url")

        return True, None


class ListBookmarksCommand(Command):
    """List all bookmarks in the DB, optionally sorting on a specific column"""

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None) -> (bool, list):
        return True, bookmarks_db.list(self.order_by)


class UpdateBookmarkCommand(Command):
    """Update a single bookmark"""

    def execute(self, data: dict[str, str | dict[str, str]]) -> (bool, None):
        bookmarks_db.edit(data, data["id"])
        return True, None


class DeleteBookmarksCommand(Command):
    """Delete a given bookmark using it's ID"""

    def execute(self, data: str) -> (bool, None):
        bookmarks_db.delete(data)
        return True, None


class QuitCommand(Command):
    """End the programmes execution safely"""

    def execute(self, data=None):
        sys.exit()
