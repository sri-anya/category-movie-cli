from faker import Faker
from models.genre import Genre
from models.movie import Movie
import random

fake = Faker()

print("seeding database")
GENRES = [
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Drama",
    "Fantasy",
    "Historical",
    "Horror",
    "Mystery",
    "Musical",
    "Romance",
    "Sci-Fi",
    "Sports",
    "Thriller",
    "War",
    "Western",
    "Documentary",
    "Family",
    "Film Noir"
]

def generate_movie_name():
    # Generate random words/phrases for the movie name
    adjective = fake.word(ext_word_list=['Dark', 'Silent', 'Amazing', 'Lost', 'Infinite', 'Brave', 'Golden', 'Mysterious', 'Eternal'])
    noun = fake.word(ext_word_list=['Journey', 'Warrior', 'Secret', 'Dream', 'Echo', 'Legacy', 'Quest', 'Realm', 'Destiny'])
    return f"The {adjective} {noun}"

def generate_random_year(start_year=1900, end_year=2023):
    return random.randint(start_year, end_year)

def generate_movie_description():
    protagonist = fake.name()
    location = fake.city()
    event = fake.sentence(nb_words=5, variable_nb_words=True)
    twist = fake.sentence(nb_words=5, variable_nb_words=True)
    return (f"{protagonist}, a resident of {location}, encounters {event.lower()} "
            f"and must navigate {twist.lower()}. An unexpected journey unfolds.")

def generate_random_genre():
    genre_name = random.choice(GENRES)
    description = f"Contains {genre_name.lower()} scenes"
    return Genre(genre_name, description)

def main():
    Genre.drop_table()
    Movie.drop_table()
    Genre.create_table()
    Movie.create_table()
    
    for genre in GENRES:
        Genre.create(genre, f"Contains {genre.lower()} scenes", fake.date() )

    for _ in range(20):
        Movie.create(generate_movie_name(), generate_random_year(),generate_movie_description(), random.randint(1, len(Genre.all)))
   

if __name__=="__main__":
    main()