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
        print("Want to add a new movie? Select option 3.")

def add_new_movie():
    print("Please enter below movie details.")
    name = input("name: ")
    release_year =(input("release year: "))
    description =input("description: ")
    genres = ", ".join(genre.name for genre in Genre.get_all())
    genre= input(f"Choose a genre from the following list: {genres}\n")
    # get genre id from genre name
    genre_id = get_genre_id(genre)
    print(f'genre_id: {genre_id}')
    movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=genre_id)
    print("new movie added successfully")
    print(movie)

def get_genre_id(genre):
    genre_returned = Genre.find_by_name(genre)
    print(f"genre_returned: {genre_returned}")
    return genre_returned.id if genre_returned else None

def delete_movie():
    movie = input("Name of the movie to be deleted?")
    movie_instance = Movie.find_by_name(movie)
    try:
        movie_instance.delete()
        print("Movie sucessfully deleted!")
    except Exception as exc:
        print(exc)

def delete_genre():
    genre = input("Name of the genre to be deleted?")
    genre_instance = Genre.find_by_name(genre)
    try:
        genre_instance.delete()
        print("Genre sucessfully deleted!")
    except Exception as exc:
        print(exc)
    
    

def exit_program():
    print("Goodbye!")
    exit()
