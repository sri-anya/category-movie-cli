# lib/models/category.py
from models.__init__ import CURSOR, CONN
from datetime import datetime

class Category:
    def __init__(self, id = None, name, description, created_at= datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at

    def __repr__(self):
        s = f"""
            {'-'*40}
            # Operator Micro-benchmarks
            # Category: {self.name}
            # Description: {self.description}
            # Created At: {self.created_at}

            {'-'*40}
            """
        return s
    
