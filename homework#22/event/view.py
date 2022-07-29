import http

import jwt
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import engine, create_engine

from config import Config
from core.auth import token_required
from core.database import db
from core.models import UserEvent
from core.models.user import User
from core.models.event import Event
from event.serializer import EventSerializer, EventInvitationSerializer, EventValidator, Status

event_router = Blueprint("event", __name__, url_prefix="/event")


@event_router.route("", methods=["GET"])
@token_required
def get(user):
    schema = EventSerializer(many=True)
    events = Event.query.filter(
        Event.users.any(
            User.id == user.id
        )
    )
    # db.session.query(Event).join(UserEvent).filter(UserEvent.user_id == user.id)
    # SELECT * FROM event JOIN user_event ON event.id = user_event.event_id WHERE user_event.user_id = 1
    events_json = schema.dump(events)
    return jsonify(events_json)


@event_router.route("/<int:event_id>", methods=["GET"])
@token_required
def retrieve(user, event_id):
    schema = EventSerializer()
    event = Event.query.filter(
        Event.users.any(
            User.id == user.id
        )
    ).filter(Event.id == event_id).first()
    # SELECT * FROM event
    # JOIN user_event ON event.id = user_event.event_id
    # WHERE user_event.user_id = 1 AND event.id = event_id

    events_json = schema.dump(event)
    return jsonify(events_json)


@event_router.route("", methods=["POST"])
@token_required
def create(user):
    data = request.get_json()
    schema = EventSerializer()
    event_data = schema.load(data)
    token = request.headers.get("Authorization")
    decrypted_data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    print(decrypted_data)
    event_obj = Event(
        name=event_data["name"],
        description=event_data["description"],
        starts_at=event_data["starts_at"],
        ends_at=event_data["ends_at"],
        creator_id=decrypted_data["user_id"]
    )
    event_obj.users.append(user)
    db.session.add(event_obj)
    db.session.commit()
    event_json = schema.dump(event_obj)
    return event_json


@event_router.route("/<int:event_id>/invite", methods=["POST"])
@token_required
def invite(user, event_id):
    data = request.get_json()
    event_schema = EventSerializer()
    invitation_schema = EventInvitationSerializer()
    invitation_data = invitation_schema.load(data)
    event = Event.query.filter(
        Event.users.any(
            User.id == user.id
        )
    ).filter(Event.id == event_id).first()

    if user.id == event.creator_id:
        for user_id in invitation_data["users_id"]:
            invited_user = User.query.get(user_id)
            if invited_user:
                event.users.append(invited_user)

    else:
        return "No event found"

    db.session.add(event)
    db.session.commit()
    event_json = event_schema.dump(event)

    for i in invitation_data["users_id"]:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
        engine.execute(f"UPDATE user_event SET status = 'PENDING' "
                       f"WHERE (user_event.event_id = {event_json['id']} AND user_event.user_id = {i})")

    return event_json


@event_router.route("/<int:event_id>/respond", methods=["POST"])
@token_required
def respond_to_invitation(user, event_id):
    data = request.get_json()
    event_validator_schema = EventValidator()
    validation_data = event_validator_schema.load(data)
    event = Event.query.filter(Event.id == event_id).first()
    if not event:
        return "No event found"

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

    status = validation_data['invitation_status']
    if status == "Accepted":
        engine.execute(f"UPDATE user_event SET status = 'ACCEPTED' "
                       f"WHERE user_event.user_id = {user.id} "
                       f"AND user_event.event_id = {event_id}")
    elif status == "Declined":
        engine.execute(f"UPDATE user_event SET status = 'DECLINED' "
                       f"WHERE user_event.user_id = {user.id} "
                       f"AND user_event.event_id = {event_id}")
    else:
        engine.execute(f"UPDATE user_event SET status = 'PENDING' "
                       f"WHERE user_event.user_id = {user.id} "
                       f"AND user_event.event_id = {event_id}")

    db.session.add(event)
    db.session.commit()
    event_validator_json = event_validator_schema.dump(validation_data)
    return event_validator_json


@event_router.route("/<int:event_id>", methods=["PUT"])
@token_required
def update(user, event_id):
    data = request.get_json()
    schema = EventSerializer()
    try:
        event_data = schema.load(data)
        event = Event.query.filter(Event.id == event_id).first()

        if user.id == event.creator_id:
            event.name = event_data["name"],
            event.description = event_data["description"],
            event.starts_at = event_data["starts_at"],
            event.ends_at = event_data["ends_at"],
            event.creator_id = user.id

            db.session.add(event)
            db.session.commit()
            event_json = schema.dump(event)
        else:
            return "Event doesn't exists", http.HTTPStatus.BAD_REQUEST
    except ValidationError as e:
        return {'errors': e.messages}, http.HTTPStatus.UNPROCESSABLE_ENTITY

    return event_json


@event_router.route("/<int:event_id>", methods=["DELETE"])
@token_required
def delete(user, event_id):
    event = Event.query.filter(Event.id == event_id).first()
    if user.id == event.creator_id:
        # event_to_del = Event.query.filter(Event.id == event_id).first()
        # UserEvent.query.filter(UserEvent.event_id == event_id).delete()
        db.session.query(UserEvent).filter(UserEvent.event_id == event_id).delete()
        db.session.query(Event).filter(Event.id == event_id).delete()
        db.session.commit()
        return {}, http.HTTPStatus.NO_CONTENT
    else:
        return "Event doesn't exists", http.HTTPStatus.BAD_REQUEST

