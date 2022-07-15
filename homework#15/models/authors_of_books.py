import os
import sys

sys.path.append(os.path.abspath('..'))

from database import db


class AuthorOfBook(db.Model):
    __tablename__ = 'author_and_book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer, db.ForeignKey("authors.id"))
    name_of_book = db.Column(db.Integer, db.ForeignKey("books.id"))
    books = db.relationship("Book")
    authors = db.relationship("Author")
