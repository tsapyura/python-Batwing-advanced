import http

from flask import Blueprint, Response, request
from marshmallow import ValidationError


from serializers.user import UserSchema

user_router = Blueprint('user', __name__, url_prefix='/user')



@user_router.route('')
def get(user):
    pass


@user_router.route('/<string:email>')
def retrieve(email):
    pass


@user_router.route('', methods=['POST'])
def create():
    data = request.get_json(force=True)

    schema = UserSchema()
    try:
        user = schema.load(data)
    except ValidationError as e:
        return {'errors': e.messages}, http.HTTPStatus.UNPROCESSABLE_ENTITY
    pass


@user_router.route('', methods=['PUT'])
def update():
    return


@user_router.route('/<string:email>', methods=['DELETE'])
def delete(email):
    pass
