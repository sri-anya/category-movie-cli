#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb
from lib.models.genre import Genre
from lib.models.movie import Movie

def reset_database():
    Genre.drop_table()
    Movie.drop_table()
    Genre.create_table()
    Movie.create_table()


reset_database()
ipdb.set_trace()
