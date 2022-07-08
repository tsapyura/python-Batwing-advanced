import os
import sys

sys.path.append(os.path.abspath('..'))

from marshmallow import Schema, fields


class AuthorsOfBooksSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    author = fields.String(required=True)
    title = fields.String(required=True)
