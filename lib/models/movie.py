# lib/models/movie.py
from models.__init__ import CURSOR, CONN
from models.genre import Genre

class Movie:

    all = {}
    
    def __init__(self, name, release_year, description, genre_id, id = None):
        self.id = id
        self.name = name
        self.release_year = release_year
        self.description = description
        self.genre_id = genre_id
 # Genre: {Genre.all[self.genre_id].name}
    def __repr__(self):
        s = f"""
            {'-'*40}
            # Movie Details
            # Name: {self.name}
            # Genre: {Genre.all[int(self.genre_id)].name}
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
            name TEXT,
            release_year INTEGER,
            description TEXT,
            genre_id INTEGER,
            FOREIGN KEY (genre_id) REFERENCES genres(id))
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
                INSERT INTO movies (name, release_year, description, genre_id)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.release_year, self.description, self.genre_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, release_year, description, genre_id):
        """ Initialize a new Movie instance and save the object to the database """
        movie = cls(name, release_year, description, genre_id)
        movie.save()
        return movie
    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Movie object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        movie = cls.all.get(row[0])
        if movie:
            # ensure attributes match row values in case local instance was modified
            movie.name = row[1]
            movie.release_year = row[2]
            movie.description = row[3]
            movie.genre_id = row[4]
        else:
            # not in dictionary, create new instance and add to dictionary
            movie = cls(row[1], row[2], row[3], row[4])
            movie.id = row[0]
            cls.all[movie.id] = movie
        return movie
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Movie object per table row"""
        sql = """
            SELECT *
            FROM movies
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id_):
        sql = """
            select * 
            from movies 
            where id = ?
            """

        row = CURSOR.execute(sql, (id_,)).fetchone()
        return Movie.instance_from_db(row)


    @classmethod
    def find_all_by_name(cls, movie_name):
        sql = """
            SELECT * 
            FROM movies
            WHERE name LIKE ?
        """

        rows = CURSOR.execute(sql,('%'+ movie_name + '%',)).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_name(cls, name):
        """Return a Movie object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM movies
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def delete(self):
        """Delete the table row corresponding to the current Movie instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM movies
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None