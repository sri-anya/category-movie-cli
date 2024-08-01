# lib/genre_helpers.py
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style
from models.movie import Movie


dict_all_genres = {} # contains {"id": Genre instance}
CURRENT_GENRE_ID = None # contains {genre id whose details are being showed currently}
CURRENT_MOVIES = {} #{movie dictionary for current genre}
genre_names = []

def handle_genres():
    display_all_genres()
    genre_id_selected = input(Fore.YELLOW+"\t\tTo learn more about particular genre, enter index of genre: "+Fore.RESET)
    print()
    global CURRENT_GENRE_ID 
    CURRENT_GENRE_ID= genre_id_selected
    selected_genre_handler()
                  
def display_all_genres():
    """
    Display all genres stored in the database.

    Retrieves all genres and prints each genre's name with an index.
    """
    genres = Genre.get_all()
    print(Fore.WHITE+ Back.LIGHTCYAN_EX+"\t\tGenres"+ Style.RESET_ALL)
    for (idx, genre) in enumerate(genres, start=1):
        genre_names.append(genre.name)
        dict_all_genres[str(idx)] = genre
        print(f'\t\t{idx}. {genre.name}')
    print()

def display_all_movies():
    
    movie_list = []
    if CURRENT_GENRE_ID in dict_all_genres.keys():
        movies = dict_all_genres[CURRENT_GENRE_ID].movies()
        if movies:
            for idx, movie in enumerate(movies, start=1):
                global CURRENT_MOVIES
                movie_list.append([idx, movie.name, movie.description])
                CURRENT_MOVIES[str(idx)] = movie
            print(Fore.WHITE+ Back.BLUE+f"\t{dict_all_genres[CURRENT_GENRE_ID].name} movies:"+Style.RESET_ALL)
            print(tabulate(movie_list, headers=["index","Name", "Description"], tablefmt="heavy_grid"))
            print()
            
        else:
            print(Fore.RED+f"\tNo movies for {dict_all_genres[CURRENT_GENRE_ID].name} genre"+Fore.RED)
        genre_movie_handler( movies=movies)
    print()

def selected_genre_handler():
   
    if CURRENT_GENRE_ID in dict_all_genres.keys():
        while True:
            genre_menu(genre_id=CURRENT_GENRE_ID)
            choice = input("\t>>")
            if choice == "0":
                exit_program()
            elif choice =="1":
                return -1
            elif choice == "2":
                display_all_movies()
            elif choice == "3":
                print(Fore.GREEN+"\n\t\tGenre Name: "+dict_all_genres[CURRENT_GENRE_ID].name+"\n"+"\t\tDescription: "+ dict_all_genres[CURRENT_GENRE_ID].description+"\n"+"\t\tCreated At: "+ dict_all_genres[CURRENT_GENRE_ID].created_at+"\n"+Fore.RESET)
    else:
        print(Fore.RED+"\t\tNo such genre exists"+Fore.RESET)
        return
    
def genre_movie_handler( movies):
    while True:
        genre_movie_menu()
        choice = input("\t\t>>")
        if choice == "0":
            exit_program()
        elif choice =="1":
            return
        elif choice == "2":
            add_movie( movies)
        elif choice == "3":
            update_movie()
        elif choice == "4":
            delete_movie()
        elif choice == "5":
            display_all_genres()
            genre_id = input(f"\n\tEnter the index of genre: ")
            global CURRENT_GENRE_ID
            CURRENT_GENRE_ID = genre_id
            break
        else:
            print(Fore.RED+"\tInvalid Choice"+Fore.RESET)

def update_movie():
    #display movies again
    movie_list = []
    movies = dict_all_genres[CURRENT_GENRE_ID].movies()
    if movies:
       
        for idx, movie in enumerate(movies, start=1):
            global CURRENT_MOVIES
            movie_list.append([idx, movie.name, movie.release_year, movie.description])
            CURRENT_MOVIES[str(idx)] = movie
        print(Fore.WHITE+ Back.BLUE+f"\t{dict_all_genres[CURRENT_GENRE_ID].name} movies:"+Style.RESET_ALL)
        print(tabulate(movie_list, headers=["","Name", "Release Year", "Description"], tablefmt="heavy_grid"))

    movie_id_selected = input(Fore.YELLOW+"\tIndex of the movie you want to update: "+Fore.RESET)
    if movie_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to update cannot be empty string\n"+Fore.RED)
        return
    
    if movie_id_selected in CURRENT_MOVIES:
        movie = CURRENT_MOVIES[movie_id_selected]
        try:
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            name = input(Fore.GREEN+"\t\tEnter the movie's new name: "+Fore.RESET)
            if name:
                movie.name = name
            else:
                movie.name = movie.name
                print(Fore.YELLOW+"\t\t"+"No change in movie's name.\n"+ Fore.RESET)
                

            release_year = input(Fore.GREEN+"\t\tEnter the movie's new release_year: "+Fore.RESET)
            if release_year:
                movie.release_year = release_year
            else:
                movie.release_year = movie.release_year
                print(Fore.YELLOW+"\t\t"+"No change in movie's release year.\n"+ Fore.RESET)

            description = input(Fore.GREEN+"\t\tEnter the movie's new description: "+Fore.RESET)
            if description:
                movie.description = description
            else:
                movie.description = movie.description
                print(Fore.YELLOW+"\t\t"+"No change in movie's description.\n"+ Fore.RESET)
            
            display_all_genres()
            genre_id = input(Fore.GREEN+"\t\tSelect the movie's new genre index: "+Fore.RESET)

            if genre_id:
                movie.genre_id = int(genre_id)
            else:
                movie.genre_id = movie.genre_id
                print(Fore.YELLOW+"\t\t"+"No change in movie's genre.\n"+ Fore.RESET)

            confirmation = input(Fore.RED+"\t\tSure about updating? Y/N: "+Fore.RESET)
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            if confirmation == 'Y':
                movie.update()
                
                print(Fore.YELLOW+"\n\t"+f'Success: Information for movie {movie.name} updated.'+ Fore.RESET)
                print("\t"+"*"*50+"\n")
                
            else:
                return
        except Exception as exc:
            print(Fore.RED+f"\t\tError updating movie. Error: {exc}\n"+Fore.RESET)
        print()
    else:
        print(Fore.RED+f"\tMovie with index {movie_id_selected} not found!! Returning to current menu..\n"+Fore.RESET)

def delete_movie():
    global CURRENT_MOVIES
    
    movie_list = []
    movies = dict_all_genres[CURRENT_GENRE_ID].movies()
    
    if movies:
    
        for idx, movie in enumerate(movies, start=1):
            
            movie_list.append([idx, movie.name, movie.description])
            
            CURRENT_MOVIES[str(idx)] = movie

        print(Fore.WHITE+ Back.BLUE+f"\t{dict_all_genres[CURRENT_GENRE_ID].name} movies:"+Style.RESET_ALL)
        print(tabulate(movie_list, headers=["","Name", "Description"], tablefmt="heavy_grid"))
    
    movie_id_selected = input(Fore.YELLOW+"\tIndex of the movie you want to delete: "+Fore.RESET)
    
    if movie_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to be deleted cannot be empty string\n"+Fore.RED)
        
        return
   
    if movie_id_selected in CURRENT_MOVIES.keys():
        movie = CURRENT_MOVIES[movie_id_selected]
        
        try:
            movie.delete()
            print(Fore.GREEN+"\tMovie sucessfully deleted!"+Fore.RESET)
        except Exception as exc:
            print(Fore.RED+f"\t\tError deleting movie. Error: {exc}\n"+Fore.RESET)
    else:
        print(Fore.RED+f"\tMovie not found! "+Fore.RESET)
    print("\t"+"*"*50+"\n")

def add_movie( movies):
    
    print(Fore.BLUE+"\tPlease enter below movie details."+Fore.RESET)
    name = input(Fore.YELLOW+"\tname: "+Fore.RESET)
    if name=="":
        print(Fore.RED+"\tSorry name cannot be empty."+Fore.RESET)
        print()
        return
    

    release_year =input(Fore.YELLOW+"\trelease year: "+Fore.RESET)
    if release_year == "":
        print(Fore.RED+"\tRelease year cannot be empty.\n"+Fore.RESET)
    description =input(Fore.YELLOW+"\tdescription: "+Fore.RESET)
    genre_id = int(CURRENT_GENRE_ID)
    
    #check if name already in movie_list
    for movie in movies:
        if movie.name == name:
            print(Fore.RED+"\tMovie with this name already present in database\n"+Fore.RESET)
            return
    try:
        movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=genre_id)
        print(Fore.GREEN+f"\t\tnew {dict_all_genres[CURRENT_GENRE_ID].name} movie added successfully"+Fore.RESET)
        print("\t"+"-"*50+"\n"+f"\t\tName: {movie.name}\n\t\tRelease_Year: {movie.release_year}\n\t\tGenre: {dict_all_genres[CURRENT_GENRE_ID].name}\n"+"\t"+"-"*50+"\n")
        
    except Exception as exc:
        print(Fore.RED +f"\t\tError creating movie. Error: {exc}"+ Fore.RESET)
    print("\t"+"*"*50+"\n")

def add_genre():
    genres = Genre.get_all()
    for genre in (genres):
        genre_names.append(genre.name)
    name = input(Fore.YELLOW+"\tEnter the genre's name: "+ Fore.RESET)
    if name in genre_names:
        print(Fore.RED + f"\tGenre {name} already exists.."+Fore.RESET)
        print()
        return
    description = input(Fore.YELLOW+"\tEnter the genre's description: "+ Fore.RESET)
    creation_date = input(Fore.YELLOW+"\tEnter the genre's creation date (YYYY-MM-DD): "+ Fore.RESET)

    try:
        genre = Genre.create(name, description, creation_date)
        print(Fore.GREEN+ f'\n\tSuccess: Genre {genre.name} is created\n'+ Fore.RESET)
        return genre
    except Exception as exc:
        print(Fore.RED + f"\tError creating genre: {exc}"+Fore.RESET)

def genre_movie_menu():
    print("\t\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t\t0. Exit Program")
    print("\t\t1. Return to previous menu")
    print(f"\t\t2. To add a new {dict_all_genres[CURRENT_GENRE_ID].name} movie")
    print(f"\t\t3. To update an/a {dict_all_genres[CURRENT_GENRE_ID].name} movie ")
    print(f"\t\t4. To delete a {dict_all_genres[CURRENT_GENRE_ID].name} movie ")
    print("\t\t5. Check another genre ")
    print()

def genre_menu(genre_id):
    print("\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t0. Exit Program")
    print("\t1. Return to main menu")
    print(f"\t2. To view all movies for {dict_all_genres[genre_id].name} genre")
    print(f"\t3. To learn more about {dict_all_genres[genre_id].name} genre ")
    print()

def delete_genre():
    display_all_genres()
    genre_id_selected = input(Fore.YELLOW+"\tIndex of the genre you want to delete: "+Fore.RESET)

    if genre_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to be deleted cannot be empty string\n"+Fore.RED)
        
        return
   
    if genre_id_selected in dict_all_genres.keys():
        genre = dict_all_genres[genre_id_selected]
        
        try:
            genre.delete()
            genre_names.remove(genre.name)
            print(Fore.GREEN+"\tGenre sucessfully deleted!"+Fore.RESET)
        except Exception as exc:
            print(Fore.RED+f"\t\tError deleting genre. Error: {exc}\n"+Fore.RESET)
    else:
        print(Fore.RED+f"\tGenre not found! "+Fore.RESET)
    print("\t"+"*"*50+"\n")
    
def exit_program():
    """
    Exit the program.

    Prints a goodbye message and exits the program.

    Returns:
        None
    """
    print("Goodbye!")
    exit()
