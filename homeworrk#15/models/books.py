import os
import sys

sys.path.append(os.path.abspath('..'))

from database import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_book = db.Column(db.String(255), nullable=False, unique=True)
