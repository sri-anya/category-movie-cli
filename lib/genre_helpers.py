# lib/genre_helpers.py
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style
from models.movie import Movie

all_genres = {}
genre_movies= {}
CURRENT_GENRE = None
CURRENT_MOVIES = {}

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
            global CURRENT_GENRE 
            CURRENT_GENRE= genre_selected
            print(CURRENT_GENRE)
            if selected_genre_handler() == -1:
                return
            else:
                continue
        elif choice == "3":
            # add_genre()
            pass
        else:
            print(Fore.RED+"\tInvalid choice.\n"+Fore.RESET)
            return
            


            

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

def display_all_movies():
    
    movie_list = []
    if CURRENT_GENRE in all_genres.keys():
        movies = all_genres[CURRENT_GENRE].movies()
        
        for idx, movie in enumerate(movies, start=1):
            global CURRENT_MOVIES
            movie_list.append([idx, movie.name, movie.description])
            genre_movies[movie.name] = movie
            CURRENT_MOVIES[str(idx)] = movie
            
            print(CURRENT_MOVIES)
        print(Fore.WHITE+ Back.BLUE+f"\t{CURRENT_GENRE} movies:"+Style.RESET_ALL)
        print(tabulate(movie_list, headers=["","Name", "Description"], tablefmt="heavy_grid"))
        genre_movie_handler( movies=movies)
    print()

def selected_genre_handler():
    
    if CURRENT_GENRE in all_genres.keys():
        while True:
            genre_menu(genre=CURRENT_GENRE)
            choice = input("\t>>")
            if choice == "0":
                exit_program()
            elif choice =="1":
                return -1
            elif choice == "2":
                display_all_movies()
            elif choice == "3":
                print(all_genres[CURRENT_GENRE].description, all_genres[CURRENT_GENRE].created_at)
    else:
        print("No such genre exists")
        return

def genre_movie_handler( movies):
    while True:
        genre_movie_menu()
        choice = input("\t>>")
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
            print(f"\tEnter the name of genre ({','.join(all_genres.keys())}): ")
            genre = input(">>")
            global CURRENT_GENRE
            CURRENT_GENRE = genre
            break
        else:
            print(Fore.RED+"Invalid Choice"+Fore.RESET)

def update_movie():
    movie_id_selected = input(Fore.YELLOW+"\tId of the movie you want to update: "+Fore.RESET)
    # movie_selected = input(Fore.YELLOW+"\tName of the movie you want to update: "+Fore.RESET)
    if movie_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to update cannot be empty string\n"+Fore.RED)
        
        return
    # for movie in movies:
    #     if movie_selected == movie.name:
    # if movie_selected in genre_movies:
    #     movie = genre_movies[movie_selected]
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

            genre_name = input(Fore.GREEN+"\t\tEnter the movie's new genre: "+Fore.RESET)

            if genre_name:
                genre_id = all_genres[genre_name].id
                movie.genre_id = genre_id
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
        print(Fore.RED+f"\tMovie {movie_id_selected} not found!! Returning to current menu..\n"+Fore.RESET)

def delete_movie():
    movie_id_selected = input(Fore.YELLOW+"\tId of the movie you want to update: "+Fore.RESET)
    # movie_selected = input(Fore.YELLOW+"\tName of the movie you want to update: "+Fore.RESET)
    if movie_id_selected == "":
        print(Fore.RED+"\tIndex of the movie selected to be deleted cannot be empty string\n"+Fore.RED)
        
        return
   
    if movie_id_selected in CURRENT_MOVIES:
        movie = CURRENT_MOVIES[movie_id_selected]
        print(movie)
        try:
            movie.delete()
            print(Fore.GREEN+"\tMovie sucessfully deleted!"+Fore.RESET)
        except Exception as exc:
            print(Fore.RED+f"\t\tError deleting movie. Error: {exc}\n"+Fore.RESET)
    else:
        print(Fore.RED+f"\tMovie {movie} not found! "+Fore.RESET)
    print("\t"+"*"*50+"\n")

def add_movie( movies):
    
    print(Fore.BLUE+"\tPlease enter below movie details."+Fore.RESET)
    name = input(Fore.YELLOW+"\tname: "+Fore.RESET)
    if name=="":
        print(Fore.RED+"\tSorry name cannot be empty."+Fore.RESET)
        print()
        return
    #check if name already in movie_list

    release_year =input(Fore.YELLOW+"\trelease year: "+Fore.RESET)
    if release_year == "":
        print(Fore.RED+"\tRelease year cannot be empty.\n"+Fore.RESET)
    description =input(Fore.YELLOW+"\tdescription: "+Fore.RESET)
    genre_id = movies[0].genre_id
    #check if name already in movie_list
    for movie in movies:
        if movie.name == name:
            print(Fore.RED+"\tMovie with this name already present\n"+Fore.RESET)
            return
    try:
        movie = Movie.create(name=name, release_year=release_year, description=description, genre_id=genre_id)
        print(Fore.GREEN+f"\t\tnew {CURRENT_GENRE} movie added successfully"+Fore.RESET)
        print("\t"+"-"*50+"\n"+f"\t\tName: {movie.name}\n\t\tRelease_Year: {movie.release_year}\n\t\tGenre: {CURRENT_GENRE}\n"+"\t"+"-"*50+"\n")
        genre_movies[movie.name] = movie
    except Exception as exc:
        print(Fore.RED +f"\t\tError creating movie. Error: {exc}"+ Fore.RESET)
    print("\t"+"*"*50+"\n")




def genre_movie_menu():
    print("\t\t",end="")
    print(Back.GREEN,"Please select an option: "+Style.RESET_ALL)
    print("\t\t0. Exit Program")
    print("\t\t1. Return to previous menu")
    print(f"\t\t2. To add a new {CURRENT_GENRE} movie")
    print(f"\t\t3. To update an/a {CURRENT_GENRE} movie ")
    print(f"\t\t4. To delete a {CURRENT_GENRE} movie ")
    print("\t\t5. Check another genre movie ")
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
    print("\t3. Add a genre")
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
