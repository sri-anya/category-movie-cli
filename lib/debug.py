#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb
from models.genre import Genre
from models.movie import Movie
from helpers import add_new_movie

def reset_database():
    Genre.drop_table()
    Movie.drop_table()
    Genre.create_table()
    Movie.create_table()

    genre1 = Genre.create("Comedy", "Contains comdey scenes")
    genre2 = Genre.create("Action", "Contains Fight scenes")
    genre3 = Genre.create("Romance", "Contains Romantic scenes")
    Movie.create("Die Hard", "Action movie example",1991, genre2.id)
    Movie.create("Golmal", "comedy  movie example",2015, genre1.id)
    Movie.create("Love Hard", "romantic movie example",2021, genre3.id)

    
reset_database()
ipdb.set_trace()
