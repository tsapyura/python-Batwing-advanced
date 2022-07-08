import os
import sys

sys.path.append(os.path.abspath('..'))

from database import db


class AuthorOfBook(db.Model):
    __tablename__ = 'author_and_book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String, nullable=False)
    name_of_book = db.Column(db.String, nullable=False)
