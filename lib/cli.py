# lib/cli.py
from pyfiglet import Figlet
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style

from helpers import (
    exit_program,
    display_all_genres, 
    find_all_by_movie_name,
    add_new_movie,
    delete_movie,
    delete_genre,
    update_genre,
    update_movie,
    display_selected_genre,
    create_genre
)


def main():
    f = Figlet(font='starwars')
    print()
    print(Fore.BLUE, f.renderText(('MovieDB').center(10," ")))
    print(Style.RESET_ALL)
    while True:
        menu()
        choice = input(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +  ">>> "+ Style.RESET_ALL)
        print()
        if choice == "0":
            exit_program()
        elif choice == "1": #GENRE
            s = f"""
            {'-'*10}
            # Genre
            {'-'*10}"""
            print(Fore.BLUE, Style.BRIGHT,s)
            print(Style.RESET_ALL)
            while True:
                show_genre_menu()
                print()
                choice = input(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +  "\t>>> "+ Style.RESET_ALL)
                
                if choice == "0":
                    print(Fore.YELLOW + "\tReturning to main menu..." + Fore.RESET)
                    print("\t"+"*"*50)
                    print()
                    break
                elif choice == "1":
                    display_all_genres()
                    x = display_selected_genre()
                    if x == -1:
                        break
                elif choice == "2":
                    print()
                    delete_genre()
                elif choice == "3":
                    print()
                    update_genre()
                elif choice == "4":
                    print()
                    create_genre()
                else:
                    print()
                    print(Fore.RED, "\tInvalid choice, returning to main menu!" + Fore.RESET)
                    print("\t"+"*"*50)
                    print()
                    break                    
        elif choice == "2": # MOVIE
            s = f"""
            {'-'*10}
            # Movie
            {'-'*10}"""
            print(Fore.BLUE, Style.BRIGHT,s)
            print(Style.RESET_ALL)
            while True:
                show_movie_menu()
                print()
                choice = input(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +  "\t>>> "+ Style.RESET_ALL)
                
                if choice == "0":
                    print(Fore.YELLOW + "\tReturning to main menu..." + Fore.RESET)
                    print("\t"+"*"*50)
                    print()
                    break
                elif choice == "1":
                    movie = input(Fore.YELLOW+ "\tEnter the movie name: "+ Fore.RESET)
                    find_all_by_movie_name(movie)
                elif choice == "2":
                    input("Enter a letter from A-Z")
                elif choice == "3":
                    add_new_movie()
                elif choice == "4":
                    delete_movie()
                elif choice == "5":
                    update_movie()
                else:
                    print(Fore.RED, "\tInvalid choice, returning to main menu!" + Fore.RESET)
                    print("\t"+"*"*50)
                    print()
                    break
        else:
            print()
            print(Fore.RED + "Invalid choice! Returning to menu..." + Fore.RESET)
            print("*"*50)
            print()


def menu():
    print(Back.GREEN,"Please select an option (0/1/2): "+Style.RESET_ALL)
    print("0. Exit the program")
    print("1. Search movies based on Genre")
    print("2. Search movies based on movie name")
    print()

def show_genre_menu():
    print("\t",end="")
    print(Back.GREEN,"Please select an option (0/1/2/3): "+Style.RESET_ALL)
    print("\t0. To return to main menu")
    print("\t1. To search using genres")
    print("\t2. Delete a genre.") 
    print("\t3. Update a genre.") 
    print("\t4. Create a genre.") 
    
def show_movie_menu():
    print("\t",end="")
    print(Back.GREEN,"Please select an option (0/1/2/3/4/5): "+Style.RESET_ALL)
    print("\t0. To return to main menu")
    print("\t1. To search using movie name")
    print("\t2. To search using letters A-Z") # pending
    print("\t3. To add a movie")
    print("\t4. To delete a movie") 
    print("\t5. To update a movie")
    # Give detail description of movie
    
if __name__ == "__main__":
    main()
