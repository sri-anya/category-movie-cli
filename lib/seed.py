from faker import Faker
from models.genre import Genre
from models.movie import Movie
import random

fake = Faker()

print("seeding database")
GENRES = [
    "Action",
    "Animation",
    "Comedy",
    "Crime",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "Family"
]

def generate_movie_name():
    """
    Generate a random movie name composed of an adjective and a noun.

    Uses Faker to generate a random adjective and noun from predefined word lists.

    Returns:
        str: A randomly generated movie name.
    """
    # Generate random words/phrases for the movie name
    adjective = fake.word(ext_word_list=['Dark', 'Silent', 'Amazing', 'Lost', 'Infinite', 'Brave', 'Golden', 'Mysterious', 'Eternal'])
    noun = fake.word(ext_word_list=['Journey', 'Warrior', 'Secret', 'Dream', 'Echo', 'Legacy', 'Quest', 'Realm', 'Destiny'])
    return f"{adjective} {noun}"

def generate_random_year(start_year=1900, end_year=2024):
    """
    Generate a random year within a given range.

    Args:
        start_year (int): The starting year of the range. Defaults to 1900.
        end_year (int): The ending year of the range. Defaults to 2024.

    Returns:
        int: A randomly generated year within the specified range.
    """
    return random.randint(start_year, end_year)

def generate_movie_description():
    """
    Generate a random movie description.

    Uses Faker to create a description involving a protagonist, a location, an event, and a twist.

    Returns:
        str: A randomly generated movie description.
    """
    protagonist = fake.name()
    location = fake.city()
    event = fake.sentence(nb_words=3, variable_nb_words=True)
    twist = fake.sentence(nb_words=3, variable_nb_words=True)
    return (f"{protagonist}, a resident of {location}, encounters {event.lower()} "
            f"and must navigate {twist.lower()}.")

def generate_random_genre():
    """
    Generate a random genre with a description.

    Selects a genre from the predefined GENRES list and creates a description for it.

    Returns:
        Genre: A Genre object with a randomly selected name and description.
    """
    genre_name = random.choice(GENRES)
    description = f"Contains {genre_name.lower()} scenes"
    return Genre(genre_name, description)

def main():
    """
    Main function to seed the database with genres and movies.

    Drops and recreates the Genre and Movie tables, then populates them with predefined genres and random movies.
    """
    Genre.drop_table()
    Movie.drop_table()
    Genre.create_table()
    Movie.create_table()
    
    for genre in GENRES:
        Genre.create(genre, f"Contains {genre.lower()} scenes", fake.date() )

    for _ in range(20):

        # if generate_movie_name() in movie_names:
        #     pass
        # else:
        Movie.create(generate_movie_name(), generate_random_year(),generate_movie_description(), random.randint(1, len(Genre.all)))
   

if __name__=="__main__":
    main()