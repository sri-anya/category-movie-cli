import sqlite3

CONN = sqlite3.connect('movie_database.db')
CURSOR = CONN.cursor()
