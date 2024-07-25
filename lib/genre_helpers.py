# lib/genre_helpers.py
from models.genre import Genre
from tabulate import tabulate
from colorama import Fore, Back, Style

def display_all_genres():
    genres = Genre.get_all()
    for (idx, genre) in enumerate(genres, start=1):
        print(f'\t{idx}. {genre.name}')
    print()

def display_selected_genre():
    genre_id_selected = int(input(Fore.YELLOW+f"\tSelect the genre (Enter 1, 2...{len(Genre.all)}): " +Fore.RESET))
    if genre_id_selected > len(Genre.all) or genre_id_selected<1:
        print(Fore.RED+ "\tSorry selected genre does not exist. Returning to main menu."+ Fore.RESET)
        print()
        return -1
    genre_selected = Genre.find_by_id(genre_id_selected)
    
    selected_movies = genre_selected.movies()
    print(Style.BRIGHT+"\tGenre Selected: "+ Fore.WHITE+Style.BRIGHT+Back.BLUE+f"{genre_selected.name}"+ Style.RESET_ALL)
    print()
    if selected_movies:
        print(Back.GREEN+"\tPlease select an option (1/2): " +Style.RESET_ALL)
        print("\t1. Sorted by Release Year")
        print("\t2. Sorted by movie name")
        print()
        sort_movies = input(Fore.MAGENTA+ Style.BRIGHT+"\t>>>"+Style.RESET_ALL)
        if sort_movies == "1":
            print(Fore.LIGHTGREEN_EX+"\tSorted by release_year"+Fore.RESET)
            sorted_movies_by_release_year = sorted(genre_selected.movies_from_db(), key=lambda movie: movie[2], reverse=True)
            print(tabulate(sorted_movies_by_release_year,headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        elif sort_movies == "2":
            print(Fore.LIGHTGREEN_EX+"\tSorted by MOVIE NAMES"+Fore.RESET)
            sorted_movies_by_name = sorted(genre_selected.movies_from_db(), key=lambda movie: movie[1])
            print(tabulate(sorted_movies_by_name,headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
        else:
            print(tabulate(genre_selected.movies_from_db(), headers=['Name' , 'release_year', 'description', 'genre_id'], tablefmt="grid", numalign="center"))
    else:
        print(Fore.RED, "\tSorry no movies for this genre!! Returning to current menu.."+Fore.RESET)
        print("\t"+"*"*50)
    print()
    return None

def delete_genre():
    genre = input(Fore.YELLOW+"\tName of the genre to be deleted: "+Fore.RESET)
    genre_instance = Genre.find_by_name(genre)
    try:
        genre_instance.delete()
        print(Fore.GREEN+"\tGenre sucessfully deleted!"+Fore.RESET)
    except Exception as exc:
        print(Fore.RED+f"\tGenre {genre} not found!! Error:{exc}. Returning to current menu.."+Fore.RESET)
        print()

def update_genre():
    genre_selected = input(Fore.YELLOW+"\tName of the genre you want to update: "+Fore.RESET)
    genre = Genre.find_by_name(genre_selected)
    if genre:
        try:
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            name = input(Fore.GREEN+"\t\tEnter the genre's new name: "+Fore.RESET)
            if name:
                genre.name = name
            else:
                genre.name = genre.name
                print(Fore.YELLOW+"\t\t"+"No change in genre's name."+ Fore.RESET)
                print()
            description = input(Fore.GREEN+"\t\tEnter the genre's new description: "+Fore.RESET)
            if description:
                genre.description = description
            else:
                genre.description = genre.description
                print(Fore.YELLOW+"\t\t"+"No change in genre's description."+ Fore.RESET)
                print()
            created_at = input(Fore.GREEN+"\t\tEnter the genre's new creation date: "+Fore.RESET)
            if created_at:
                genre.created_at = created_at
            else:
                genre.created_at = genre.created_at
                print(Fore.YELLOW+"\t\t"+"No change in genre's creation date."+ Fore.RESET)
                print()
            
            confirmation = input(Fore.RED+"\t\tSure about updating? Y/N: "+Fore.RESET)
            print(Fore.GREEN+"\t\t"+"-"*40+Fore.RESET)
            if confirmation == 'Y':
                genre.update()
                print()
                print(Fore.YELLOW+"\t"+f'Success: Information for genre {genre.name} updated.'+ Fore.RESET)
                print("\t"+"*"*50+"\n")
                
            else:
                return
        except Exception as exc:
            print(Fore.RED+f"\tError updating genre: {name}. Error: {exc}"+Fore.RESET)
    else:
        print(Fore.RED+f"\tGenre {genre_selected} not found!! Returning to current menu.."+Fore.RESET)
        print()

def create_genre():
    name = input(Fore.YELLOW+"\tEnter the genre's name: "+ Fore.RESET)
    if Genre.find_by_name(name) and (Genre.find_by_name(name)).id in Genre.all:
        print(Fore.RED + f"\tGenre {name} already exists.."+Fore.RESET)
        print()
        return
    else:
        description = input(Fore.YELLOW+"\tEnter the genre's description: "+ Fore.RESET)
        creation_date = input(Fore.YELLOW+"\tEnter the genre's creation date: "+ Fore.RESET)

        try:
            genre = Genre.create(name, description, creation_date)
            print(Fore.GREEN+ f'\tSuccess: Genre {genre.name} is created'+ Fore.RESET)
        except Exception as exc:
            print(Fore.RED + f"\tError creating genre: {name}. Error: {exc} "+Fore.RESET)

    print()