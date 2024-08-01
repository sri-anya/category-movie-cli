# lib/models/movie.py
from models.__init__ import CURSOR, CONN
from models.genre import Genre

class Movie:

    all = {}
    
    
    def __init__(self, name, release_year, description, genre_id, id = None):
        """
        Initialize a new Movie instance.
        
        Parameters:
            name (str): The name of the movie.
            release_year (int): The release year of the movie.
            description (str): The description of the movie.
            genre_id (int): The ID of the genre associated with the movie.
            id (int, optional): The ID of the movie in the database.
        """
        self.id = id
        self.name = name
        self.release_year = release_year
        self.description = description
        self.genre_id = genre_id
        
    def __repr__(self):
        """
        Return a string representation of the Movie instance, displaying details about the movie.
        
        Returns:
            str: The string representation of the Movie instance.
        """
        s = f"""
            {'-'*40}
            # Movie Details
            # Name: {self.name}
            # Genre: {(Genre.find_by_id(self.genre_id)).name}
            # Release Year: {self.release_year}
            {'-'*40}
            """
        return s
    
    @property
    def name(self):
        """
        Get the name of the movie.
        
        Returns:
            str: The name of the movie.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of the movie.
        
        Parameters:
            value (str): The new name of the movie.
        
        Raises:
            ValueError: If the name is not a non-empty string.
        """
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def release_year(self):
        """
        Get the release year of the movie.
        
        Returns:
            int: The release year of the movie.
        """
        return self._release_year

    @release_year.setter
    def release_year(self, value):
        """
        Set the release year of the movie.
        
        Parameters:
            value (int): The new release year of the movie.
        
        Raises:
            ValueError: If the release year is not between 1900 and 2024.
        """
        if  int(value) <=2024 and int(value)>=1900:
            self._release_year = value
        else:
            raise ValueError(
                "Release_year should be an integer value between 1900 and 2024"
            )

    @property
    def genre_id(self):
        """
        Get the genre ID of the movie.
        
        Returns:
            int: The genre ID of the movie.
        """
        return self._genre_id

    @genre_id.setter
    def genre_id(self, genre_id):
        """
        Set the genre ID of the movie.
        
        Parameters:
            genre_id (int): The new genre ID of the movie.
        
        Raises:
            ValueError: If the genre ID does not reference a valid genre.
        """
        if type(genre_id) is int and Genre.find_by_id(genre_id):
            self._genre_id = genre_id
        else:
            raise ValueError(
                "genre_id must reference a genre in the database")
    
    @classmethod
    def create_table(cls):
        """
        Create a new table to persist the attributes of Movie instances.
        """
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
        """
        Drop the table that persists Movie instances.
        """
        sql = """
            DROP TABLE IF EXISTS movies;
        """
        CURSOR.execute(sql)
        CONN.commit()
    

    def save(self):
        """
        Insert a new row with the name, release_year, description, and genre_id values of the current Movie object.
        Update the object id attribute using the primary key value of the new row.
        Save the object in the local dictionary using the table row's primary key as the dictionary key.
        """
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
        """
        Initialize a new Movie instance and save the object to the database.
        
        Parameters:
            name (str): The name of the movie.
            release_year (int): The release year of the movie.
            description (str): The description of the movie.
            genre_id (int): The ID of the genre associated with the movie.
        
        Returns:
            Movie: The newly created Movie instance.
        """
        movie = cls(name, release_year, description, genre_id)
        movie.save()
        return movie
    
    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Movie object having the attribute values from the table row.
        
        Parameters:
            row (tuple): A tuple containing the values of a row from the movies table.
        
        Returns:
            Movie: The corresponding Movie instance.
        """
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
        """
        Return a list containing one Movie object per table row.
        
        Returns:
            list: A list of Movie objects.
        """
        sql = """
            SELECT *
            FROM movies
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id_):
        """
        Find a Movie instance by its ID.
        
        Parameters:
            id_ (int): The ID of the movie to find.
        
        Returns:
            Movie: The corresponding Movie instance, or None if not found.
        """
        sql = """
            select * 
            from movies 
            where id = ?
            """

        row = CURSOR.execute(sql, (id_,)).fetchone()
        return Movie.instance_from_db(row)
    
    def delete(self):
        """
        Delete the table row corresponding to the current Movie instance,
        delete the dictionary entry, and reassign id attribute
        """

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

   
    def update(self):
        """Update the table row corresponding to the current Movie instance."""
        sql = """
            UPDATE movies
            SET name = ?, release_year = ?, description = ?, genre_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.release_year, self.description, self.genre_id, self.id))
        CONN.commit()