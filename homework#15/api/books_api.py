import os
import sys

sys.path.append(os.path.abspath('..'))

import http

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from database import db
from models.books import Book
from serializers.books import BookSchema

book_router = Blueprint('book', __name__, url_prefix='/book')


@book_router.route('')
def get():
    book_schema = BookSchema()

    book = Book.query.order_by(Book.id)
    books_json = book_schema.dump(book, many=True)
    return jsonify(books_json)


@book_router.route('/<int:id_>')
def retrieve(id_):
    book_schema = BookSchema()
    book = Book.query.filter_by(id=id_).first()
    if not book is None:  # add validation
        book_json = book_schema.dump(book)
        return jsonify(book_json)
    else:
        return "Book doesn't exists", http.HTTPStatus.BAD_REQUEST


@book_router.route('', methods=['POST'])
def create():
    data = request.get_json(force=True)

    schema = BookSchema()
    try:
        book_data = schema.load(data)
        new_book = Book(title=book_data['title'])
        db.session.add(new_book)
        db.session.commit()

        new_book_json = schema.dump(new_book)
    except ValidationError as e:
        return {'errors': e.messages}, http.HTTPStatus.UNPROCESSABLE_ENTITY

    return new_book_json


@book_router.route('/<int:id_>', methods=['PUT'])
def update(id_):
    data = request.get_json(force=True)

    schema = BookSchema()
    try:
        book_data = schema.load(data)
        book = Book.query.filter_by(id=id_).first()
        if not book is None:  # add validation
            book.title = book_data['title']
            db.session.add(book)
            db.session.commit()

            new_book_json = schema.dump(book)
        else:
            return "Book doesn't exists", http.HTTPStatus.BAD_REQUEST
    except ValidationError as e:
        return {'errors': e.messages}, http.HTTPStatus.UNPROCESSABLE_ENTITY

    return new_book_json


@book_router.route('/<int:id_>', methods=['DELETE'])
def delete(id_):
    book = Book.query.filter_by(id=id_).first()
    if not book is None:  # add validation
        Book.query.filter_by(id=id_).delete()
        db.session.commit()
        return {}, http.HTTPStatus.NO_CONTENT
    else:
        return "Book doesn't exists", http.HTTPStatus.BAD_REQUEST