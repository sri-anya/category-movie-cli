#!/usr/bin/env python3
# lib/cli.py
from pyfiglet import Figlet
from colorama import Fore, Back, Style
from genre_helpers import  (
    handle_genres
    )
    
from movie_helpers import (
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
        
def menu():
    """
    Display the main menu.

    Provides options for the user to exit the program, manage genres, or search for movies.

    Returns:
        None
    """
    print(Back.GREEN,"Please select an option (0/1/2): "+Style.RESET_ALL)
    print("0. Exit the program")
    print("1. Search movies based on Genre")
    print("2. Search movies based on movie name")
    print()



    
def movie_menu():
    """
    Display the movie menu.

    Provides options for the user to return to the main menu, search for movies by name or initial letter,
    add, delete, or update movies.

    Returns:
        None
    """
    print("\t",end="")
    print(Back.GREEN,"Please select an option (0/1/2/3/4/5): "+Style.RESET_ALL)
    print("\t0. To return to main menu")
    print("\t1. To search using movie name")
    print("\t2. To search using letters A-Z") 
    print("\t3. To add a movie")
    print("\t4. To delete a movie") 
    print("\t5. To update a movie+\n")
    
    
if __name__ == "__main__":
    main()
