#!/usr/bin/env python3
# lib/debug.py

import ipdb
from models.genre import Genre
from models.movie import Movie

def reset_database():
    """
    Reset the database by dropping and recreating the Genre and Movie tables.

    Creates sample genres and movies to populate the newly created tables.
    """
    Genre.drop_table()
    Movie.drop_table()
    Genre.create_table()
    Movie.create_table()

    genre1 = Genre.create("Comedy", "Contains comdey scenes")
    genre2 = Genre.create("Action", "Contains Fight scenes")
    genre3 = Genre.create("Romance", "Contains Romantic scenes")
    Movie.create("Die Hard",1991, "Action movie example", genre2.id)
    Movie.create("Golmal", 2015,"comedy  movie example", genre1.id)
    Movie.create("Hangover", 2009,"comedy  movie example 2", genre1.id)
    Movie.create("Love Hard", 2021,"romantic movie example", genre3.id)

    
reset_database()
ipdb.set_trace()
