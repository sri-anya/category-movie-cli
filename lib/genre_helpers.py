# lib/genre_helpers.py
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style

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
            # add_movie()
            pass
        elif choice == "3":
            # update_movie(movie)
            pass
        elif choice == "4":
            # delete_movie()
            pass
        else:
            print(Fore.RED+"Invalid Choice"+Fore.RESET)
        


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
    print("\t1. Return to main menu")
    print(f"\t2. To add a movie for {genre} genre")
    print(f"\t3. To update a movie from {genre} genre ")
    print(f"\t4. To delete a movie from {genre} genre ")
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
