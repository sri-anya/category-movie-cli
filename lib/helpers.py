# lib/helpers.py
from models.genre import Genre
from models.movie import Movie
from tabulate import tabulate
from colorama import Fore, Back, Style

def display_all_genres():
    genres = Genre.get_all()
    for (idx, genre) in enumerate(genres, start=1):
        print(f'\t{idx}. {genre.name}')
    print()

def display_selected_genre():
    genre_id_selected = int(input(f"Select the genre (Enter 1, 2, 3...{len(Genre.all)}): "))
    if genre_id_selected > len(Genre.all) or genre_id_selected<1:
        print("""Sorry selected genre does not exist. Returning to main menu.""")
        return -1
    genre_selected = Genre.find_by_id(genre_id_selected)
    
    selected_movies = genre_selected.movies()
    print(f"Checkout {genre_selected.name} movies")
    if selected_movies:
        # for movie in selected_movies:
        #     print(f"""
        #     {movie.name} """)
        # print("")
        print("Want to sort selected movies by release_year?")
        sorted_movies_by_release_year = sorted(genre_selected.movies_from_db(), key=lambda movie: movie[2], reverse=True)
        print(tabulate(sorted_movies_by_release_year,headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        # sorted_movies_by_name = sorted(genre_selected.movies(), key=lambda movie: movie.name)
        # print(sorted_movies_by_name)
    else:
        print(Fore.RED, "Sorry no movies for this genre!!")
        print(Fore.RESET)
    return None

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
    except:
        print(f"Genre {genre} not found")

def update_genre():
    id_ = input("Enter the genre's id: ")
    genre = Genre.find_by_id(id_)
    if genre:
        try:
            name = input("Enter the genre's new name: ")
            genre.name = name
            description = input("Enter the genre's new description: ")
            genre.description = description
            created_at = input("Enter the genre's new creation date: ")
            genre.created_at = created_at

            genre.update()
            print(f'Success: {genre}')
        except Exception as exc:
            print("Error updating genre: ", exc)
    else:
        print(f'Genre {id_} not found')

def update_movie():
    id_ = input("Enter the movie's id: ")
    if movie := Movie.find_by_id(id_):
        try:
            name = input("Enter the movie's new name: ")
            movie.name = name
            release_year = input("Enter the movie's new release_year: ")
            movie.release_year = release_year
            description = input("Enter the movie's new description: ")
            movie.description = description
            genre_id = input("Enter the movie's new genre: ")
            movie.genre_id = genre_id
            
            movie.update()
            print(f'Success: {movie}')
        except Exception as exc:
            print("Error updating movie: ", exc)
    else:
        print(f'Movie {id_} not found')
    
    

def exit_program():
    print("Goodbye!")
    exit()
