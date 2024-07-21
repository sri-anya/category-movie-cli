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
    Movie.create("Die Hard",1991, "Action movie example", genre2.id)
    Movie.create("Golmal", 2015,"comedy  movie example", genre1.id)
    Movie.create("Hangover", 2009,"comedy  movie example 2", genre1.id)
    Movie.create("Love Hard", 2021,"romantic movie example", genre3.id)

    
reset_database()
ipdb.set_trace()
