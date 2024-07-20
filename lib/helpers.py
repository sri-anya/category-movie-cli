# lib/helpers.py
from models.genre import Genre
from models.movie import Movie

def display_all_genres():
    genres = Genre.get_all()
    for (idx, genre) in enumerate(genres, start=1):
        print(f'{idx}. {genre.name}')
    print()

def find_all_by_movie_name(movie_name):
    movies = Movie.find_all_by_name(movie_name)
    if movies:
        for movie in movies:
            print(movie)
    else:
        print("Sorry no movies available!")
        print("Want to add a new movie?")

def helper_3():
    print("Performing useful function#3.")


def exit_program():
    print("Goodbye!")
    exit()
