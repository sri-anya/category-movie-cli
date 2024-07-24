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
        print(tabulate(movies, headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        # for movie in movies:
        #     print(movie)
    else:
        print(Fore.RED+"\tSorry no movies available!"+ Fore.RESET)
        print(Fore.BLUE+"\tWant to add a new movie? Select option 3 from the menu."+Fore.RESET)
        print("\t"+"*"*50)
    print()

def add_new_movie():
    print(Fore.BLUE+"\tPlease enter below movie details.")
    name = input(Fore.YELLOW+"\tname: "+Fore.RESET)
    if name=="":
        print(Fore.RED+"\tSorry name cannot be empty."+Fore.RESET)
        print()
        return
    release_year =input(Fore.YELLOW+"\trelease year: "+Fore.RESET)
    description =input(Fore.YELLOW+"\tdescription: "+Fore.RESET)
    genres = ", ".join(genre.name for genre in Genre.get_all())
    genre= input(Fore.YELLOW+"\tChoose a genre from the following list: "+ Fore.LIGHTMAGENTA_EX+ f"{genres}"+"\n"+Style.RESET_ALL)
    # get genre id from genre name
    genre_id = get_genre_id(genre)
    if genre_id:
        movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=genre_id)
        print(Fore.GREEN+"\t\tnew movie added successfully"+Fore.RESET)
        print(movie)
    else:
        print(Fore.RED+"\tGenre not found.. Returning to current menu...")
        print("\t"+"*"*50)
        print()
        return
    print("\t"+"*"*50)
    print()

def get_genre_id(genre):
    genre_returned = Genre.find_by_name(genre)
    return genre_returned.id if genre_returned else None

def delete_movie():
    print()
    movie = input(Fore.YELLOW+"\tName of the movie to be deleted?"+Fore.RESET)
    movie_instance = Movie.find_by_name(movie)
    try:
        movie_instance.delete()
        print(Fore.GREEN+"\tMovie sucessfully deleted!"+Fore.RESET)
    except Exception:
        print(Fore.RED+f"\tMovie {movie} not found! "+Fore.RESET)
    print("\t"+"*"*50)
    print()

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
    genre_selected = input(Fore.YELLOW+"\tName of the genre you want to update: "+Fore.RESET)
    genre = Genre.find_by_name(genre_selected)
    if genre:
        try:
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            name = input(Fore.GREEN+"\t\tEnter the genre's new name: "+Fore.RESET)
            if name:
                genre.name = name
            else:
                genre.name = genre.name
                print(Fore.YELLOW+"\t\t"+"No change in genre name."+ Fore.RESET)
                print()
            description = input(Fore.GREEN+"\t\tEnter the genre's new description: "+Fore.RESET)
            if description:
                genre.description = description
            else:
                genre.description = genre.description
                print(Fore.YELLOW+"\t\t"+"No change in genre description."+ Fore.RESET)
                print()
            created_at = input(Fore.GREEN+"\t\tEnter the genre's new creation date: "+Fore.RESET)
            if created_at:
                genre.created_at = created_at
            else:
                genre.created_at = genre.created_at
                print(Fore.YELLOW+"\t\t"+"No change in genre creation date."+ Fore.RESET)
                print()
            
            confirmation = input(Fore.RED+"\t\tSure about updating? Y/N: "+Fore.RESET)
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            if confirmation == 'Y':
                genre.update()
                print()
                print(Fore.YELLOW+"\t"+f'Success: Information for genre {genre.name} updated.'+ Fore.RESET)
                print("\t"+"*"*50+"\n")
                
            else:
                return
        except:
            print(Fore.RED+f"\tError updating genre."+Fore.RESET)
    else:
        print(Fore.RED+f"\tGenre {genre_selected} not found!! Returning to current menu.."+Fore.RESET)
        print()

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


def create_genre():
    name = input(Fore.YELLOW+"\tEnter the genre's name: "+ Fore.RESET)
    if (Genre.find_by_name(name)).id in Genre.all:
        print(Fore.RED + f"\tGenre {name} already exists.."+Fore.RESET)
        print()
        return
    description = input(Fore.YELLOW+"\tEnter the genre's description: "+ Fore.RESET)
    creation_date = input(Fore.YELLOW+"\tEnter the genre's creation date: "+ Fore.RESET)

    try:
        genre = Genre.create(name, description, creation_date)
        print(Fore.GREEN+ f'\tSuccess: Genre {genre.name} is created'+ Fore.RESET)
    except Exception as exc:
        print(Fore.RED + f"\tError creating genre: "+Fore.RESET)
    
    

def exit_program():
    print("Goodbye!")
    exit()
