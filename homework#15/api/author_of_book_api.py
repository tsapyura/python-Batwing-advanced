import os
import sys

sys.path.append(os.path.abspath(".."))

import http

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from database import db
from models.authors_of_books import AuthorOfBook
from models.books import Book
from models.authors import Author
from serializers.authors_of_books import AuthorsOfBooksSchema
from serializers.authors import AuthorSchema
from serializers.books import BookSchema

author_of_book_router = Blueprint("author_and_book", __name__, url_prefix="/author_and_book")


@author_of_book_router.route("")
def get():
    author_of_book_schema = AuthorsOfBooksSchema()

    author_of_book = AuthorOfBook.query.order_by(AuthorOfBook.id)
    author_of_book_json = author_of_book_schema.dump(author_of_book, many=True)
    return jsonify(author_of_book_json)


@author_of_book_router.route("/<int:id_>")
def retrieve(id_):
    author_of_book_schema = AuthorsOfBooksSchema()
    author_of_book = AuthorOfBook.query.filter_by(id=id_).first()
    author_of_book_json = author_of_book_schema.dump(author_of_book)
    return jsonify(author_of_book_json)


@author_of_book_router.route("/<int:author_id>/<int:book_id>", methods=["POST"])
def create(book_id, author_id):
    author_schema = AuthorSchema()
    author1 = Author.query.filter_by(id=author_id).first()
    book_schema = BookSchema()
    title = Book.query.filter_by(id=book_id).first()
    schema = AuthorsOfBooksSchema()

    if author1 is not None and title is not None:
        book_json = book_schema.dump(title)
        author_json = author_schema.dump(author1)

        new_author_of_book = AuthorOfBook(author=author_json["name_lastname"], name_of_book=book_json["name_of_book"])
        db.session.add(new_author_of_book)
        db.session.commit()
        print(new_author_of_book)
        new_author_of_book_json = schema.dump(new_author_of_book)

        return jsonify(new_author_of_book_json)
    elif author1 is None:
        return "This author does not exists"
    elif title is None:
        return "This book does not exists"


@author_of_book_router.route("/<int:id_>/<int:author_id>/<int:book_id>", methods=["PUT"])
def update(id_, author_id, book_id):
    author_schema = AuthorSchema()
    author = Author.query.filter_by(id=author_id).first()

    book_schema = BookSchema()
    book = Book.query.filter_by(id=book_id).first()

    schema = AuthorsOfBooksSchema()
    author_of_book = AuthorOfBook.query.filter_by(id=id_).first()

    if not author is None and not book is None:
        book_json = book_schema.dump(book)
        author_json = author_schema.dump(author)
        author_of_book.author = author_json["name_lastname"],
        author_of_book.title = book_json["title"]
        db.session.add(author_of_book)
        db.session.commit()

        new_author_of_book_json = schema.dump(author_of_book)

        return jsonify(new_author_of_book_json)
    elif author is None:
        return "This author does not exists"
    elif book is None:
        return "This book does not exists"


@author_of_book_router.route("/<int:id_>", methods=["DELETE"])
def delete(id_):
    author_of_book = AuthorOfBook.query.filter_by(id=id_).first()
    if not author_of_book is None:
        AuthorOfBook.query.filter_by(id=id_).delete()
        db.session.commit()
        return {}, http.HTTPStatus.NO_CONTENT
    else:
        return "Record doesn't exists", http.HTTPStatus.BAD_REQUEST
