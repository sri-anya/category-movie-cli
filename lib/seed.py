from faker import Faker
from models.genre import Genre
from models.movie import Movie
from random import choice
fake = Faker()

print("seeding database")

def main():
    genre1 = Genre.create("Comdey", "Contains comdey scenes")
    genre2 = Genre.create("Action", "Contains Fight scenes")
    Movie.create("Die Hard", 1991,"Action movie example", genre2.id)
    Movie.create("Golmal",2015, "comedy  movie example", genre1.id)
    for i in range(4):
        pass



if __name__=="__main__":
    main()