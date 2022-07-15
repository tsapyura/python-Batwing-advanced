import os
import sys

sys.path.append(os.path.abspath('..'))

from marshmallow import Schema, fields
from marshmallow.validate import Length


class BookSchema(Schema):
    id = fields.Integer(required=True, load_only=True)
    name_of_book = fields.String(required=True, validate=Length(max=255))
