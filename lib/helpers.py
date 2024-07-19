# lib/helpers.py
from models.genre import Genre
from models.movie import Movie

def display_all_genres():
    genres = Genre.get_all()
    for (idx, genre) in enumerate(genres, start=1):
        print(f'{idx}. {genre.name}')
    print()

def helper_2():
    print("Performing useful function#2.")

def helper_3():
    print("Performing useful function#3.")


def exit_program():
    print("Goodbye!")
    exit()
