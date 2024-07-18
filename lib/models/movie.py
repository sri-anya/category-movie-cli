# lib/models/movie.py
from models.__init__ import CURSOR, CONN

class Movie:
    def __init__(self, id, name, release_year, description, genre_id):
        self.id = id
        self.name = name
        self.release_year = release_year
        self.description = description
        self.genre_id = genre_id

    def __repr__(self):
        s = f"""
            {'-'*40}
            # Movie Details
            # Name: {self.name}
            # Genre: {self.genre_id}
            # Release Year: {self.release_year}
            {'-'*40}
            """
        return s
    
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Movie instances """
        sql = """
            CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            release_year INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Movie instances """
        sql = """
            DROP TABLE IF EXISTS movies;
        """
        CURSOR.execute(sql)
        CONN.commit()
    

    def save(self):
        """ Insert a new row with the name, release_year, description and genre id values of the current Movie object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO employees (name, release_year, description, genre_id)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.release_year, self.description, self.genre_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self