# lib/helpers.py
from models.genre import Genre
from models.movie import Movie
from tabulate import tabulate
from colorama import Fore, Back, Style

def find_all_by_movie_name(movie_name):
    movies = Movie.find_all_by_name(movie_name)
    if movies:
        print(tabulate(movies, headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
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
        try:
            movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=genre_id)
            print(Fore.GREEN+"\t\tnew movie added successfully"+Fore.RESET)
            print(movie)
        except Exception as exc:
            print(Fore.RED +f"\t\tError creating movie. Error: {exc}"+ Fore.RESET)
    else:
        print(Fore.RED+"\tGenre not found.. Returning to current menu...")
        print("\t"+"*"*50)
        print()
        return
    print("\t"+"*"*50)
    print()

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

def update_movie():
    movie_selected = input(Fore.YELLOW+"\tName of the movie you want to update: "+Fore.RESET)
    if movie_selected == "":
        print(Fore.RED+"\tName of the movie to update cannot be empty string"+Fore.RED)
        print()
        return
    if movie := Movie.find_by_name(movie_selected):
        try:
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            name = input(Fore.GREEN+"\t\tEnter the movie's new name: "+Fore.RESET)
            if name:
                movie.name = name
            else:
                movie.name = movie.name
                print(Fore.YELLOW+"\t\t"+"No change in movie's name."+ Fore.RESET)
                print()

            release_year = input(Fore.GREEN+"\t\tEnter the movie's new release_year: "+Fore.RESET)
            if release_year:
                movie.release_year = release_year
            else:
                movie.release_year = movie.release_year
                print(Fore.YELLOW+"\t\t"+"No change in movie's release year."+ Fore.RESET)
                print()
            
            description = input(Fore.GREEN+"\t\tEnter the movie's new description: "+Fore.RESET)
            if description:
                movie.description = description
            else:
                movie.description = movie.description
                print(Fore.YELLOW+"\t\t"+"No change in movie's description."+ Fore.RESET)
                print()
            genre_name = input(Fore.GREEN+"\t\tEnter the movie's new genre: "+Fore.RESET)
            
            if genre_name:
                genre_id = Genre.find_by_name(genre_name).id
                movie.genre_id = genre_id
            else:
                movie.genre_id = movie.genre_id
                print(Fore.YELLOW+"\t\t"+"No change in movie's genre."+ Fore.RESET)
                print()
            confirmation = input(Fore.RED+"\t\tSure about updating? Y/N: "+Fore.RESET)
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            if confirmation == 'Y':
                movie.update()
                print()
                print(Fore.YELLOW+"\t"+f'Success: Information for movie {movie.name} updated.'+ Fore.RESET)
                print("\t"+"*"*50+"\n")
                print()
            else:
                return
        except Exception as exc:
            print(Fore.RED+"\t\tError updating movie."+Fore.RESET)
            print()
    else:
        print(Fore.RED+f"\tMovie {movie_selected} not found!! Returning to current menu.."+Fore.RESET)
        print()

def get_genre_id(genre):
    genre_returned = Genre.find_by_name(genre)
    return genre_returned.id if genre_returned else None    

def search_by_AZ():
    character = input(Fore.YELLOW+"\tEnter a character: "+ Fore.RESET)
    if character.isalpha():
        movies = Movie.find_all_by_first_char(character=character)
        if movies:
            print(tabulate(movies, headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        # for movie in movies:
        #     print(movie)
        else:
            print(Fore.RED+"\tSorry no movies available!"+ Fore.RESET)
            print(Fore.BLUE+"\tWant to add a new movie? Select option 3 from the menu."+Fore.RESET)
            print("\t"+"*"*50)
        print()
    else:
        print(Fore.RED+"\tInvalid character.."+ Fore.RESET)
        print()
        


def exit_program():
    print("Goodbye!")
    exit()
