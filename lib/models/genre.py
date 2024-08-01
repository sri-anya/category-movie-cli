# lib/models/genre.py
from models.__init__ import CURSOR, CONN
from datetime import datetime

class Genre:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__( self, name, description, created_at, id = None):
        """
        Initialize a new Genre instance.

        Parameters:
            name (str): The name of the genre.
            description (str): The description of the genre.
            created_at (str): The creation date of the genre in 'YYYY-MM-DD' format.
            id (int, optional): The ID of the genre in the database.
        """

        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at

    def __repr__(self):
        """
        Return a string representation of the Genre instance, displaying details about the genre.

        Returns:
            str: The string representation of the Genre instance.
        """
        s = f"""
            {'-'*40}
            # Genre Information
            # Genre: {self.name}
            # Description: {self.description}
            # Created At: {self.created_at}
            {'-'*40}
            """
        return s
    
    @property
    def name(self):
        """
        Get the name of the genre.

        Returns:
            str: The name of the genre.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of the genre.

        Parameters:
            value (str): The new name of the genre.

        Raises:
            ValueError: If the name is not a non-empty string or contains only digits.
        """
        if isinstance(value, str) and not value.isdigit() and len(value):
            self._name = value
        else:
            raise ValueError(
                "Name of genre cannot be empty and must contains strings."
            )
        
    @property
    def description(self):
        """
        Get the description of the genre.

        Returns:
            str: The description of the genre.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the description of the genre.

        Parameters:
            value (str): The new description of the genre.

        Raises:
            ValueError: If the description contains only digits.
        """
        if isinstance(value, str) and not value.isdigit():
            self._description = value
        else:
            raise ValueError(
                "Description of genre cannot be only numbers."
            )
        
    @property
    def created_at(self):
        """
        Get the creation date of the genre.

        Returns:
            str: The creation date of the genre in 'YYYY-MM-DD' format.
        """
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        """
        Set the creation date of the genre.

        Parameters:
            value (str): The new creation date of the genre.

        Raises:
            ValueError: If the date is not in the 'YYYY-MM-DD' format.
        """
        if value=="":
            self._created_at=datetime.now().strftime('%Y-%m-%d')
        elif value !="" and datetime.strptime(value, "%Y-%m-%d"):
            self._created_at = value
        else:
            raise ValueError(
                "Incorrect data format, should be YYYY-MM-DD"
            )
    
    @classmethod
    def create_table(cls):
        """
        Create a new table to persist the attributes of Genre instances.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            created_at DATE)
        """

        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """
        Drop the table that persists Genre instances.
        """
        sql = """
            DROP TABLE IF EXISTS genres;
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """
        Insert a new row with the name, description, and created_at values of the current Genre instance.
        Update the object id attribute using the primary key value of the new row.
        Save the object in the local dictionary using the table row's primary key as the dictionary key.
        """
        sql = """
            INSERT INTO genres (name, description, created_at)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.description, self.created_at))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, description, created_at=datetime.now().strftime('%Y-%m-%d')):
        """
        Initialize a new Genre instance and save the object to the database.

        Parameters:
            name (str): The name of the genre.
            description (str): The description of the genre.
            created_at (str): The creation date of the genre in 'YYYY-MM-DD' format.

        Returns:
            Genre: The newly created Genre instance.
        """
        genre = cls(name, description, created_at)
        genre.save()
        return genre
    
    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Genre object having the attribute values from the table row.

        Parameters:
            row (tuple): A tuple containing the values of a row from the genres table.

        Returns:
            Genre: The corresponding Genre instance.
        """

        # Check the dictionary for an existing instance using the row's primary key
        genre = cls.all.get(row[0])
        if genre:
            # ensure attributes match row values in case local instance was modified
            genre.name = row[1]
            genre.description = row[2]
            genre.created_at = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            genre = cls(row[1], row[2], row[3])
            genre.id = row[0]
            cls.all[genre.id] = genre
        return genre

    @classmethod
    def get_all(cls):
        """
        Return a list containing a Genre object per row in the table.

        Returns:
            list: A list of Genre objects.
        """
        sql = """
            SELECT *
            FROM genres
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id_):
        """
        Find a Genre instance by its ID.

        Parameters:
            id_ (int): The ID of the genre to find.

        Returns:
            Genre: The corresponding Genre instance, or None if not found.
        """
        sql = """
            select * 
            from genres 
            where id = ?
            """

        row = CURSOR.execute(sql, (id_,)).fetchone()
        return Genre.instance_from_db(row)
    
    
    # @classmethod
    # def find_by_name(cls, name):
    #     """
    #     Return a Genre object corresponding to the first table row matching the specified name.

    #     Parameters:
    #         name (str): The name of the genre to find.

    #     Returns:
    #         Genre: The corresponding Genre instance, or None if not found.
    #     """
    #     sql = """
    #         SELECT *
    #         FROM genres
    #         WHERE name is ?
    #     """

    #     row = CURSOR.execute(sql, (name,)).fetchone()
    #     return cls.instance_from_db(row) if row else None
    
    def movies(self):
        """
        Return a list of Movie instances that belong to the current Genre instance.

        Returns:
            list: A list of Movie instances.
        """
        from models.movie import Movie
        sql = """
            select * 
            from movies
            where genre_id = ?
        """

        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Movie.instance_from_db(row) for row in rows]
    
    def delete(self):
        """
        Delete the table row corresponding to the current Genre instance,
        delete the dictionary entry, and reassign the id attribute.
        """

        sql = """
            DELETE FROM genres
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
    
    def update(self):
        """
        Update the table row corresponding to the current Genre instance.
        """
        sql = """
            UPDATE genres
            SET name = ?, description = ?, created_at = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.description, self.created_at, self.id))
        CONN.commit()

   