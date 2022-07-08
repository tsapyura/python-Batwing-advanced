import os
import sys

sys.path.append(os.path.abspath('..'))

from marshmallow import Schema, fields
from marshmallow.validate import Length


class AuthorSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    name_lastname = fields.String(required=True, validate=Length(max=255))