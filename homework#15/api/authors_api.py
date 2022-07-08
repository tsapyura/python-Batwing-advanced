import os
import sys

sys.path.append(os.path.abspath('..'))

import http

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from database import db
from models.authors import Author
from serializers.authors import AuthorSchema

author_router = Blueprint('author', __name__, url_prefix='/author')


@author_router.route('')
def get():
    author_schema = AuthorSchema()

    authors = Author.query.order_by(Author.id)
    authors_json = author_schema.dump(authors, many=True)
    return jsonify(authors_json)


@author_router.route('/<int:id_>')
def retrieve(id_):
    author_schema = AuthorSchema()
    author = Author.query.filter_by(id=id_).first()
    if not author is None:  # add validation
        author_json = author_schema.dump(author)
        return jsonify(author_json)
    else:
        return "Author doesn't exists", http.HTTPStatus.BAD_REQUEST


@author_router.route('', methods=['POST'])
def create():
    data = request.get_json(force=True)

    schema = AuthorSchema()
    try:
        author_data = schema.load(data)
        new_author = Author(name_lastname=author_data['name_lastname'])
        db.session.add(new_author)
        db.session.commit()

        new_author_json = schema.dump(new_author)
    except ValidationError as e:
        return {'errors': e.messages}, http.HTTPStatus.UNPROCESSABLE_ENTITY

    return new_author_json


@author_router.route('/<int:id_>', methods=['PUT'])
def update(id_):
    data = request.get_json(force=True)

    schema = AuthorSchema()
    try:
        author_data = schema.load(data)
        author = Author.query.filter_by(id=id_).first()
        if not author is None:  # add validation
            author.name_lastname = author_data['name_lastname']
            db.session.add(author)
            db.session.commit()

            new_author_json = schema.dump(author)
        else:
            return "Author doesn't exists", http.HTTPStatus.BAD_REQUEST
    except ValidationError as e:
        return {'errors': e.messages}, http.HTTPStatus.UNPROCESSABLE_ENTITY

    return new_author_json


@author_router.route('/<int:id_>', methods=['DELETE'])
def delete(id_):
    author = Author.query.filter_by(id=id_).first()
    if not author is None:  # add validation
        Author.query.filter_by(id=id_).delete()
        db.session.commit()
        return {}, http.HTTPStatus.NO_CONTENT
    else:
        return "Author doesn't exists", http.HTTPStatus.BAD_REQUEST