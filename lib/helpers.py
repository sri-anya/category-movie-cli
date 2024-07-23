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
    genre_id_selected = int(input(Fore.YELLOW+f"\tSelect the genre (Enter 1, 2...{len(Genre.all)}): " +Fore.RESET))
    if genre_id_selected > len(Genre.all) or genre_id_selected<1:
        print(Fore.RED+ "\tSorry selected genre does not exist. Returning to main menu."+ Fore.RESET)
        print()
        return -1
    genre_selected = Genre.find_by_id(genre_id_selected)
    
    selected_movies = genre_selected.movies()
    print(Style.BRIGHT+"\tGenre Selected: "+ Fore.WHITE+Style.BRIGHT+Back.BLUE+f"{genre_selected.name}"+ Style.RESET_ALL)
    print()
    if selected_movies:
        print(Back.GREEN+"\tPlease select an option (1/2): " +Style.RESET_ALL)
        print("\t1. Sorted by Release Year")
        print("\t2. Sorted by movie name")
        print()
        sort_movies = input(Fore.MAGENTA+ Style.BRIGHT+"\t>>>"+Style.RESET_ALL)
        if sort_movies == "1":
            print(Fore.LIGHTGREEN_EX+"\tSorted by release_year"+Fore.RESET)
            sorted_movies_by_release_year = sorted(genre_selected.movies_from_db(), key=lambda movie: movie[2], reverse=True)
            print(tabulate(sorted_movies_by_release_year,headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        elif sort_movies == "2":
            print(Fore.LIGHTGREEN_EX+"\tSorted by MOVIE NAMES"+Fore.RESET)
            sorted_movies_by_name = sorted(genre_selected.movies_from_db(), key=lambda movie: movie[1])
            print(tabulate(sorted_movies_by_name,headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        else:
            print(tabulate(genre_selected.movies_from_db(), headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
    else:
        print(Fore.RED, "\tSorry no movies for this genre!! Returning to current menu.."+Fore.RESET)
        print("\t"+"*"*50)
    print()
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
    genre = input(Fore.YELLOW+"\tName of the genre to be deleted: "+Fore.RESET)
    genre_instance = Genre.find_by_name(genre)
    try:
        genre_instance.delete()
        print(Fore.GREEN+"\tGenre sucessfully deleted!"+Fore.RESET)
    except:
        print(Fore.RED+f"\tGenre {genre} not found!! Returning to current menu.."+Fore.RESET)
        print()

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
            print(Fore.RED+f"\tError updating genre"+Fore.RESET)
    else:
        print(Fore.RED+f"\tGenre {id_} not found!! Returning to current menu.."+Fore.RESET)

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
