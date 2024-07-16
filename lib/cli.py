# lib/cli.py
from pyfiglet import Figlet

from helpers import (
    exit_program,
    helper_1
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        else:
            print("Invalid choice")


def menu():
    
    f = Figlet(font='starwars')
    print("\n")
    print(f.renderText(('MOVIE MATRIX').center(20," ")))
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")


if __name__ == "__main__":
    main()
