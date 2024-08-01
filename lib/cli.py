#!/usr/bin/env python3
# lib/cli.py
from pyfiglet import Figlet
from colorama import Fore, Back, Style
from genre_helpers import  (
    handle_genres,
    add_genre,
    delete_genre
    )
    
from movie_helpers import (
    movie_main,
    exit_program
    )

def main():
    """
    Main function to run the CLI application.

    Displays the main menu and handles user input for navigating the application.
    Users can select options to manage genres and movies, or exit the program.

    Returns:
        None
    """
    f = Figlet(font='starwars')
    print()
    print(Fore.BLUE, f.renderText(('MovieDB').center(10," ")))
    print(Style.RESET_ALL)
    while True:
        menu()
        choice = input(">>>")
        if choice == "0":
            exit_program()
        elif choice == "1":
            handle_genres()
        elif choice =="2":
            movie_main()
        elif choice =="3":
            add_genre()
        elif choice =="4":
            delete_genre()
        else:
            print("Invalid choice!")
        
def menu():
    """
    Display the main menu.

    Provides options for the user to exit the program, manage genres, or search for movies.

    Returns:
        None
    """
    print(Back.GREEN,"Please select an option (0/1/2/3/4): "+Style.RESET_ALL)
    print("0. Exit the program")
    print("1. Display all genres")
    print("2. Display all movies")
    print("3. Add a genre")
    print("4. Delete a genre")
    print()
    
    
if __name__ == "__main__":
    main()
