"""The main CLI code for bark"""

import commands


class Option:
    """Class to contain menu options for display"""

    def __init__(self, display_name: str, command, preparation=None):
        self.display_name = display_name
        self.command = command
        self.preparation = preparation

    def choose(self):
        data = self.preparation() if self.preparation else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.display_name


def print_options(options):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")


if __name__ == "__main__":
    print("Welcome to Bark!")
    commands.CreateBookmarksTableCommand().execute()
    options = {
        "A": Option("Add a bookmark", commands.AddBookmarksCommand()),
        "L": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option(
            "List bookmarks by title", commands.ListBookmarksCommand(order_by="title")
        ),
        "D": Option("Delete bookmark", commands.DeleteBookmarksCommand()),
        "Q": Option("Quit Bark", commands.QuitCommand()),
    }
    print_options(options)
