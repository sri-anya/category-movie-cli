#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb
from models.genre import Genre
from models.movie import Movie

def reset_database():
    Genre.drop_table()
    Movie.drop_table()
    Genre.create_table()
    Movie.create_table()

    genre1 = Genre.create("Comdey", "Contains comdey scenes")
    genre2 = Genre.create("Action", "Contains Fight scenes")
    Movie.create("Die Hard", 1991,"Action movie example", genre2.id)
    Movie.create("Golmal",2015, "comedy  movie example", genre1.id)



reset_database()
ipdb.set_trace()
