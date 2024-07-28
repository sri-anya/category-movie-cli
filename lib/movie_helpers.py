# lib/helpers.py
from models.genre import Genre
from models.movie import Movie
from tabulate import tabulate
from colorama import Fore, Back, Style



def display_all_movies():
    movie_list = []
    movies = Movie.get_all()
        
    for idx, movie in enumerate(movies, start=1):
        
        movie_list.append([idx, movie.name, movie.description])
        
    print(Fore.WHITE+ Back.BLUE+"\tAll movies:"+Style.RESET_ALL)
    print(tabulate(movie_list, headers=["index","Name", "Description"], tablefmt="heavy_grid"))
    # genre_movie_handler( movies=movies)
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
