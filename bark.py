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


def print_options(options: dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")


def user_choice_is_valid(choice: str, options: dict[str, Option]) -> bool:
    return choice in options or choice.upper() in options


def get_user_choice(options: dict[str, Option]) -> Option:
    user_choice = input("Please choose an option: ")
    while not user_choice_is_valid(user_choice, options):
        print("Invalid choice.")
        user_choice = input("Please choose an option: ")
    return options[user_choice.upper()]


def get_user_input(prompt: str, required=True) -> str:
    user_input = input(f"{prompt}: ") or None
    while required and not user_input:
        print("Insufficient input. Please provide a value")
        user_input = input(f"{prompt}: ") or None
    return user_input


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
    user_choice = get_user_choice(options)
    user_choice.choose()
