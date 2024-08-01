# lib/helpers.py
from models.genre import Genre
from genre_helpers import (dict_all_genres, display_all_genres, add_genre)
from models.movie import Movie
from tabulate import tabulate
from colorama import Fore, Back, Style

all_movies = {} #{idx: Movie instance}
movie_name_dict = {} #{movie name: Movie Instance}
dict_all_genres = {} # {idx:genre}

def display_all_movies():
    movie_list = []
    movies = Movie.get_all()
    genres = Genre.get_all()
    for (idx, genre) in enumerate(genres, start=1):
        dict_all_genres[str(idx)] = genre

    for idx, movie in enumerate(movies, start=1):
        
        movie_list.append([idx, movie.name, movie.description, dict_all_genres[str(movie.genre_id)].name])
        all_movies[str(idx)] = movie
        movie_name_dict[movie.name] = movie
    print(Fore.WHITE+ Back.BLUE+"\tAll movies:"+Style.RESET_ALL)
    print(tabulate(movie_list, headers=["index","Name", "Description","Genre"], tablefmt="heavy_grid"))
    print()

def add_movie():
    print(Fore.BLUE+"\tPlease enter below movie details."+Fore.RESET)
    name = input(Fore.YELLOW+"\tname: "+Fore.RESET)
    if name=="":
        print(Fore.RED+"\tSorry name cannot be empty."+Fore.RESET)
        print()
        return

    release_year =input(Fore.YELLOW+"\tRelease year: "+Fore.RESET)
    if release_year == "":
        print(Fore.RED+"\tRelease year cannot be empty.\n"+Fore.RESET)
    description =input(Fore.YELLOW+"\tdescription: "+Fore.RESET)

    print(Fore.YELLOW+"\tSelect Genre index from below list: "+Fore.RESET)
    display_all_genres()
    genre_id = input("\t>>")
    
    if genre_id in dict_all_genres.keys():
        genre_name = dict_all_genres[genre_id].name
    else:
        print(Fore.RED +"\tPlease select genre from above list only. Returning to menu.."+Fore.RESET)
        return
    
        
    #check if name already in movie_list
    for movie_name in movie_name_dict.keys():
        if  movie_name_dict[movie_name].name == name and movie_name_dict[movie_name].genre_id == int(genre_id):
            print(Fore.RED+"\tMovie with this name and genre already present in database\n"+Fore.RESET)
            return
    try:
        movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=int(genre_id))
        movie_name_dict[name]=movie
        print(Fore.GREEN+f"\t\tnew {genre_name} movie added successfully"+Fore.RESET)
        print("\t"+"-"*50+"\n"+f"\t\tName: {movie.name}\n\t\tRelease_Year: {movie.release_year}\n\t\tGenre: {genre_name}\n"+"\t"+"-"*50+"\n")
        
    except Exception as exc:
        print(Fore.RED +f"\t\tError creating movie. Error: {exc}"+ Fore.RESET)
    print("\t"+"*"*50+"\n")

def delete_movie():
    
    movie_id_selected = input(Fore.YELLOW+"\tIndex of the movie you want to delete: "+Fore.RESET)
   
    if movie_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to be deleted cannot be empty string\n"+Fore.RED)
        
        return
   
    if movie_id_selected in all_movies.keys():
        movie = all_movies[movie_id_selected]
        
        try:
            movie.delete()
            print(Fore.GREEN+"\tMovie sucessfully deleted!"+Fore.RESET)
        except Exception as exc:
            print(Fore.RED+f"\t\tError deleting movie. Error: {exc}\n"+Fore.RESET)
    else:
        print(Fore.RED+f"\tMovie not found! "+Fore.RESET)
    print("\t"+"*"*50+"\n")

def update_movie():
    movie_id_selected = input(Fore.YELLOW+"\tIndex of the movie you want to update: "+Fore.RESET)
    if movie_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to be updated cannot be empty string\n"+Fore.RED)
        
        return
   
    if movie_id_selected in all_movies.keys():
        movie = all_movies[movie_id_selected]
        
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
            
            print(Fore.YELLOW+"\tSelect Genre index from below list: "+Fore.RESET)
            display_all_genres()
            genre_id = input("\t>>")
            
            
            if genre_id:
                if genre_id in dict_all_genres.keys():
                    
                    movie.genre_id = int(genre_id)
                else:
                    print("Genre index incorrect!")
               
                
                
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
            print(Fore.RED+f"\t\tError updating movie. Error: {exc}"+Fore.RESET)
            print()
    else:
        print(Fore.RED+f"\tMovie with index {movie_id_selected} not found!! Returning to current menu.."+Fore.RESET)
        print()

def find_all_by_movie_name():
    word = input(Fore.YELLOW+"\tEnter the search word/movie name: "+Fore.RESET)
    movies = []
    for movie_name, movie in movie_name_dict.items():
        if word in movie_name:
            movies.append([movie.name,movie.description])

    if movies:
        print(tabulate(movies, headers=["Name", "Description"], tablefmt="heavy_grid"))
    else:
        print(Fore.RED+"\tSorry no movies available!"+ Fore.RESET)
        print(Fore.BLUE+"\tWant to add a new movie? Select option 3 from the menu."+Fore.RESET)
        print("\t"+"*"*50)
    print()

def movie_main():
    display_all_movies()
    while True:
        
        menu()
        choice = input("\t>>")
        if choice == "0":
            exit_program()
        elif choice == "1":
            return
        elif choice == "2":
            find_all_by_movie_name()
        elif choice == "3":
            add_movie()
        elif choice == "4":
            delete_movie()
        elif choice == "5":
            update_movie()
        elif choice == "6":
            display_all_movies()
        else:
            print("Invalid choice")

def menu():
    
    """
    Display the movie menu.

    Provides options for the user to return to the main menu, search for movies by name or initial letter,
    add, delete, or update movies.

    Returns:
        None
    """
    print("\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t0. Exit Program")
    print("\t1. Return to main menu")
    print("\t2. To search using movie name")
    print("\t3. To add a movie")
    print("\t4. To delete a movie") 
    print("\t5. To update a movie")
    print("\t6. To display all movies"+"\n")

def exit_program():
    """
    Exit the program.

    Prints a goodbye message and exits the program.

    Returns:
        None
    """
    print("Goodbye!")
    exit()
