# lib/genre_helpers.py
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style
from models.movie import Movie

all_genres = {}

def handle_genres():
    while True:
        menu()
        choice = input(">>")
        if choice == "0":
            exit_program()
        elif choice =="1":
            return
        elif choice =="2":
            display_all_genres()
            genre_selected = input(Fore.YELLOW+"\tTo learn more about particular genre type name of genre:"+Fore.RESET)
            selected_genre_handler(genre_selected=genre_selected)
            


            

def display_all_genres():
    """
    Display all genres stored in the database.

    Retrieves all genres and prints each genre's name with an index.
    """
    genres = Genre.get_all()
    print(Fore.WHITE+ Back.LIGHTCYAN_EX+"\tGenres"+ Style.RESET_ALL)
    for (idx, genre) in enumerate(genres, start=1):
        all_genres[genre.name] = genre
        print(f'\t{idx}. {genre.name}')
    print()



def selected_genre_handler(genre_selected):
    while True:
        genre_menu(genre=genre_selected)
        choice = input("\t\t>>")
        if choice == "0":
            exit_program()
        elif choice =="1":
            return
        elif choice == "2":
            display_all_movies(genre_selected=genre_selected)
        elif choice == "3":
            print(all_genres[genre_selected].description, all_genres[genre_selected].created_at)

def genre_movie_handler(genre, movies):
    while True:
        genre_movie_menu(genre=genre)
        choice = input("\t\t>>")
        if choice == "0":
            exit_program()
        elif choice =="1":
            return
        elif choice == "2":
            add_movie(genre, movies)
        elif choice == "3":
            # update_movie(movie)
            pass
        elif choice == "4":
            # delete_movie()
            pass
        else:
            print(Fore.RED+"Invalid Choice"+Fore.RESET)
def update_movie(genre, movies):
    movie_selected = input(Fore.YELLOW+"\tName of the movie you want to update: "+Fore.RESET)
    if movie_selected == "":
        print(Fore.RED+"\tName of the movie to update cannot be empty string"+Fore.RED)
        print()
        return
    for movie in movies:
        if movie_selected != movie.name:
            print(Fore.RED+f"\tMovie {movie_selected} not found!! Returning to current menu.."+Fore.RESET)
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

def add_movie(genre, movies):
    # print(genre, movies[0].genre_id)
    # print(all_genres)
    print(Fore.BLUE+"\tPlease enter below movie details."+Fore.RESET)
    name = input(Fore.YELLOW+"\tname: "+Fore.RESET)
    if name=="":
        print(Fore.RED+"\tSorry name cannot be empty."+Fore.RESET)
        print()
        return
    #check if name already in movie_list

    release_year =input(Fore.YELLOW+"\trelease year: "+Fore.RESET)
    if release_year == "":
        print(Fore.RED+"\tRelease year cannot be empty.\n"+Fore.RESET)
    description =input(Fore.YELLOW+"\tdescription: "+Fore.RESET)
    genre_id = movies[0].genre_id
    #check if name already in movie_list
    for movie in movies:
        if movie.name == name:
            print(Fore.RED+"\tMovie with this name already present\n"+Fore.RESET)
            return
    try:
        movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=genre_id)
        print(Fore.GREEN+f"\t\tnew {genre} movie added successfully"+Fore.RESET)
        print("\t"+"-"*50+"\n"+f"\t\tName: {movie.name}\n\t\tRelease_Year: {movie.release_year}\n\t\tGenre: {genre}"+"\t"+"-"*50+"\n")
    except Exception as exc:
        print(Fore.RED +f"\t\tError creating movie. Error: {exc}"+ Fore.RESET)
    print("\t"+"*"*50+"\n")


def display_all_movies(genre_selected):
    movie_list = []
    if genre_selected in all_genres.keys():
        movies = all_genres[genre_selected].movies()
        for idx, movie in enumerate(movies, start=1):
            movie_list.append([idx, movie.name, movie.description])
        print(f"\t{genre_selected} movies:")
        print(tabulate(movie_list, headers=["","Name", "Description"], tablefmt="heavy_grid"))
        genre_movie_handler(genre=genre_selected, movies=movies)
    print()

def genre_movie_menu(genre):
    print("\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t0. Exit Program")
    print("\t1. Return to previous menu")
    print(f"\t2. To add a new {genre} movie")
    print(f"\t3. To update an/a {genre} movie ")
    print(f"\t4. To delete a {genre} movie ")
    print("\t5. Check another genre movie ")
    print()

def genre_menu(genre):
    print("\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t0. Exit Program")
    print("\t1. Return to main menu")
    print(f"\t2. To view all movies for {genre} genre")
    print(f"\t3. To learn more about {genre} genre ")
    print()

def menu():
    """
    Display the genre menu.

    Provides options for the user to return to the main menu, search for genres, delete, update, or create genres.

    Returns:
        None
    """
    print("\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t0. Exit Program")
    print("\t1. Return to main menu")
    print("\t2. Display all genres")
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
