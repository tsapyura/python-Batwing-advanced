import enum

from sqlalchemy import Enum

from core.database import db


class Status(enum.Enum):
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    PENDING = 'PENDING'


class UserEvent(db.Model):
    __tablename__ = 'user_event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    invitation_status = db.Column(db.Enum(Status))
