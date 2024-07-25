# lib/models/genre.py
from models.__init__ import CURSOR, CONN
from datetime import datetime

class Genre:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__( self, name, description, created_at, id = None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at

    def __repr__(self):
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
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and not value.isdigit() and len(value):
            self._name = value
        else:
            raise ValueError(
                "Name of genre cannot be empty and must contains strings."
            )
        
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str) and not value.isdigit():
            self._description = value
        else:
            raise ValueError(
                "Description of genre cannot be only numbers."
            )
        
    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
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
        """ Create a new table to persist the attributes of Genre instances """
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
        """ Create a new table to persist the attributes of Genre instances """
        sql = """
            DROP TABLE IF EXISTS genres;
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, description and created_at values of the current Genre instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
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
        """ Initialize a new Genre instance and save the object to the database """
        genre = cls(name, description, created_at)
        genre.save()
        return genre
    

    @classmethod
    def instance_from_db(cls, row):
        """Return a Genre object having the attribute values from the table row."""

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
        """Return a list containing a Genre object per row in the table"""
        sql = """
            SELECT *
            FROM genres
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id_):
        sql = """
            select * 
            from genres 
            where id = ?
            """

        row = CURSOR.execute(sql, (id_,)).fetchone()
        return Genre.instance_from_db(row)
    
    
    @classmethod
    def find_by_name(cls, name):
        """Return a Genre object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM genres
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def movies(self):
        from models.movie import Movie
        sql = """
            select * 
            from movies
            where genre_id = ?
        """

        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Movie.instance_from_db(row) for row in rows]
    
    def delete(self):
        """Delete the table row corresponding to the current Genre instance,
        delete the dictionary entry, and reassign id attribute"""

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
        """Update the table row corresponding to the current Genre instance."""
        sql = """
            UPDATE genres
            SET name = ?, description = ?, created_at = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.description, self.created_at, self.id))
        CONN.commit()

    def movies_from_db(self):
        from models.movie import Movie
        sql = """
            select * 
            from movies
            where genre_id = ?
        """

        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return rows