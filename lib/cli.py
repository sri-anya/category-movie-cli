# lib/cli.py
from pyfiglet import Figlet

from helpers import (
    exit_program,
    display_all_genres, 
    find_all_by_movie_name
)


def main():
    f = Figlet(font='starwars')
    print(f.renderText(('MovieDB').center(10," ")))
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            s = f"""
                {'-'*40}
                # Genre
                {'-'*40}
                """
            print(s)
            while True:
                show_genre_menu()
                choice = input("> ")
                if choice == "0":
                    break
                elif choice == "1":
                    display_all_genres()
                    
        elif choice == "2":
            s = f"""
                {'-'*40}
                # Movie
                {'-'*40}
                """
            print(s)
            while True:
                show_movie_menu()
                choice = input("> ")
                if choice == "0":
                    break
                elif choice == "1":
                    movie = input("Enter movie name: ")
                    find_all_by_movie_name(movie)
            
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Search movies based on Genre")
    print("2. Search movies based on movie name")

def show_genre_menu():
    print("0. To return to main menu")
    print("1. To search using genres")
    
def show_movie_menu():
    print("0. To return to main menu")
    print("1. To search using movie name")
    print("2. To search using letters A-Z")




if __name__ == "__main__":
    main()
