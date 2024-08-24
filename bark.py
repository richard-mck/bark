"""The main CLI code for bark"""

import commands


class Options:
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


if __name__ == "__main__":
    print("Welcome to Bark!")
    commands.CreateBookmarksTableCommand().execute()
