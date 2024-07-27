# lib/helpers.py
from models.genre import Genre
from models.movie import Movie
from tabulate import tabulate
from colorama import Fore, Back, Style

def display_all_movies():
    """
    Display all genres stored in the database.

    Retrieves all genres and prints each genre's name with an index.
    """
    genres = Movie.get_all()
    print(Fore.WHITE+ Back.LIGHTCYAN_EX+"\tMovies"+ Style.RESET_ALL)
    for (idx, genre) in enumerate(genres, start=1):
        all_genres[genre.name] = genre
        print(f'\t{idx}. {genre.name}')
    print()

def exit_program():
    """
    Exit the program.

    Prints a goodbye message and exits the program.

    Returns:
        None
    """
    print("Goodbye!")
    exit()
