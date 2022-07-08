import os
import sys

sys.path.append(os.path.abspath('..'))

from database import db


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_lastname = db.Column(db.String(255), nullable=False, unique=True)
