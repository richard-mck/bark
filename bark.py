"""The main CLI code for bark"""

import commands

if __name__ == "__main__":
    print("Welcome to Bark!")
    commands.CreateBookmarksTableCommand().execute()
