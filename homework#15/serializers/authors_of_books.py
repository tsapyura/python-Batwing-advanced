import os
import sys

from serializers.authors import AuthorSchema
from serializers.books import BookSchema

sys.path.append(os.path.abspath('..'))

from marshmallow import Schema, fields


class AuthorsOfBooksSchema(Schema):
    id = fields.Integer(required=True, load_only=True)
    authors = fields.Nested(AuthorSchema())
    books = fields.Nested(BookSchema())
