import jwt
from flask import request

from config import Config
from core.models.user import User


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "Token required"}, 401

        # try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        # except Exception:
        #     return {"error": "token is invalid"}, 401

        current_user = User.query.filter_by(id=data["user_id"]).first()
        return f(current_user, *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
