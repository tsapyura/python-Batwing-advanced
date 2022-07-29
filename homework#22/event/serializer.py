import enum

from marshmallow import Schema, fields

from user.serializer import UserSerializer


class EventSerializer(Schema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    starts_at = fields.DateTime()
    ends_at = fields.DateTime()
    creator_id = fields.Integer()
    users = fields.List(fields.Nested(UserSerializer))


class EventInvitationSerializer(Schema):
    users_id = fields.List(fields.Integer)


class Status(enum.Enum):
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    PENDING = 'PENDING'

class EventValidator(Schema):
    invitation_status = fields.String()
