# lib/cli.py
from pyfiglet import Figlet
from models.genre import Genre

from helpers import (
    exit_program,
    display_all_genres, 
    find_all_by_movie_name,
    add_new_movie
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
                    genre_id_selected = int(input("Select the genre (Enter 1, 2, 3...): "))
                    genre_selected = Genre.find_by_id(genre_id_selected-1)
                    print(genre_selected.movies)

                    
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
                elif choice == "2":
                    input("Enter a letter from A-Z")
                elif choice == "3":
                    add_new_movie()
                else:
                    print("Invalid choice! returning to main menu.")
                    break
            
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
    # sort particular genre movie by year, or, aplhabetically
    
def show_movie_menu():
    print("0. To return to main menu")
    print("1. To search using movie name")
    print("2. To search using letters A-Z")
    print("3. To add a movie")




if __name__ == "__main__":
    main()
