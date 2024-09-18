"""The main CLI code for bark"""

import os

import commands


class Option:
    """Class to contain menu options for display"""

    def __init__(self, display_name: str, command, preparation=None):
        self.display_name = display_name
        self.command = command
        self.preparation = preparation

    def choose(self):
        data = self.preparation() if self.preparation else None
        message = self.command.execute(data)
        if isinstance(message, list):
            print_bookmarks(message)
        else:
            print(message)

    def __str__(self):
        return self.display_name


def print_bookmarks(bookmarks):
    for bookmark in bookmarks:
        print("\t".join(str(field) if field else "" for field in bookmark))


def print_options(options: dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")


def user_choice_is_valid(choice: str, options: dict[str, Option]) -> bool:
    return choice in options or choice.upper() in options


def get_menu_choice(options: dict[str, Option]) -> Option:
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


def get_bookmark_id_for_deletion() -> str:
    return get_user_input("Enter bookmark ID")


def get_new_bookmark_data() -> dict[str, str]:
    return {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes (optional)", required=False),
    }


def get_github_import_data() -> dict[str, str]:
    return {
        "github_username": get_user_input("Github username"),
        "keep_timestamps": get_user_input("Keep star timestamp Y/n", required=False) in ("Y", "y", None),
    }


def get_bookmark_to_update() -> dict[str, str | dict[str, str]]:
    bookmark_id = get_user_input("Bookmark ID to update")
    bookmark_field = get_user_input("Field to update[title, url, notes]")
    new_value = get_user_input(f"New {bookmark_field}")
    return {"id": bookmark_id, "update": {bookmark_field: new_value}}


def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)


def bark_loop():
    options = {
        "A": Option(
            "Add a bookmark",
            commands.AddBookmarksCommand(),
            preparation=get_new_bookmark_data,
        ),
        "G": Option(
            "Import GitHub stars",
            commands.ImportGitHubStarsCommand(),
            preparation=get_github_import_data,
        ),
        "L": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option("List bookmarks by title", commands.ListBookmarksCommand(order_by="title")),
        "U": Option(
            "Update bookmark",
            commands.UpdateBookmarkCommand(),
            preparation=get_bookmark_to_update,
        ),
        "D": Option(
            "Delete bookmark",
            commands.DeleteBookmarksCommand(),
            preparation=get_bookmark_id_for_deletion,
        ),
        "Q": Option("Quit Bark", commands.QuitCommand()),
    }
    print_options(options)
    menu_choice = get_menu_choice(options)
    clear_screen()
    menu_choice.choose()
    _ = input("Press enter to return to menu")


if __name__ == "__main__":
    clear_screen()
    print("Welcome to Bark!")
    commands.CreateBookmarksTableCommand().execute()
    while True:
        bark_loop()
