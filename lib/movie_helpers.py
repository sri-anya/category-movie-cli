# lib/helpers.py
from models.genre import Genre
from models.movie import Movie
from tabulate import tabulate
from colorama import Fore, Back, Style

def exit_program():
    """
    Exit the program.

    Prints a goodbye message and exits the program.

    Returns:
        None
    """
    print("Goodbye!")
    exit()
