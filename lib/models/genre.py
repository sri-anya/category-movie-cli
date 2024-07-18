# lib/models/genre.py
from models.__init__ import CURSOR, CONN
from datetime import datetime

class Genre:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__( self, name, description, created_at= datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id = None):
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
            CREATE TABLE IF EXISTS genres;
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, description and created_at values of the current Genre instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO departments (name, description, created_at)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.description, self.created_at))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, description, created_at):
        """ Initialize a new Department instance and save the object to the database """
        genre = cls(name, description, created_at)
        genre.save()
        return genre
    
