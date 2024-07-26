# lib/genre_helpers.py
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style

all_genres = {}



def handle_genres():
    while True:
        genre_menu()
        choice = input(">>")
        if choice == "0":
            exit_program()
        elif choice =="1":
            return
        elif choice =="2":
            display_all_genres()
            print("\tmovies for genre")
            

def display_all_genres():
    """
    Display all genres stored in the database.

    Retrieves all genres and prints each genre's name with an index.
    """
    genres = Genre.get_all()
    print(Fore.WHITE+ Back.LIGHTBLUE_EX+"\tGenres"+ Style.RESET_ALL)
    for (idx, genre) in enumerate(genres, start=1):
        all_genres[genre.name] = [genre.description,genre.created_at]
        print(f'\t{idx}. {genre.name}')
    print()

def genre_menu():
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
