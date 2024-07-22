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
    update_movie
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
        elif choice == "1":
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
                    genre_id_selected = int(input(f"Select the genre (Enter 1, 2, 3...{len(Genre.all)}): "))
                    if genre_id_selected > len(Genre.all) or genre_id_selected<1:
                        print("""
                              Sorry selected genre does not exist. Returning to main menu.
                              """)
                        break
                    genre_selected = Genre.find_by_id(genre_id_selected)
                    print(f"Checkout {genre_selected.name} movies")
                    selected_movies = genre_selected.movies()
                    if selected_movies:
                        for movie in selected_movies:
                            print(f"""
                            {movie.name} """)
                        print("")
                        print("Want to sort selected movies by release_year?")
                        sorted_movies_by_release_year = sorted(genre_selected.movies_from_db(), key=lambda movie: movie[2], reverse=True)
                        print(tabulate(sorted_movies_by_release_year,headers=['Name' , 'release_year', 'description', 'genre_id']))
                        sorted_movies_by_name = sorted(genre_selected.movies(), key=lambda movie: movie.name)
                        print(sorted_movies_by_name)
                    else:
                        print(Fore.RED, "Sorry no movies for this genre!!")
                        print(Fore.RESET)
                elif choice == "2":
                    delete_genre()
                elif choice == "3":
                    update_genre()
                else:
                    print()
                    print(Fore.RED, "\tInvalid choice, returning to main menu!" + Fore.RESET)
                    print("\t"+"*"*50)
                    print()
                    break                    
        elif choice == "2":
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
                    movie = input("Enter movie name: ")
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
    print(Back.GREEN,"Please select an option (0/1/2):", end=" ")
    print(Back.RESET)
    print("0. Exit the program")
    print("1. Search movies based on Genre")
    print("2. Search movies based on movie name")
    print()

def show_genre_menu():
    print("\t",end="")
    print(Back.GREEN,"Please select an option (0/1/2/3):", end=" ")
    print(Back.RESET)
    print("\t0. To return to main menu")
    print("\t1. To search using genres")
    # sort particular genre movie by year, or, aplhabetically
    print("\t2. Delete a genre.") 
    print("\t3. Update a genre.") 
    
def show_movie_menu():
    print("\t",end="")
    print(Back.GREEN,"Please select an option (0/1/2/3/4/5):", end=" ")
    print(Back.RESET)
    print("\t0. To return to main menu")
    print("\t1. To search using movie name")
    print("\t2. To search using letters A-Z") # pending
    print("\t3. To add a movie")
    print("\t4. To delete a movie") 
    print("\t5. To update a movie")
    # Give detail description of movie
if __name__ == "__main__":
    main()
