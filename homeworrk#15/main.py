import http

from flask import Flask

from config import Config
from database import db
from api.authors_api import author_router
from api.books_api import book_router
from api.author_of_book_api import author_of_book_router


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(author_router)
    app.register_blueprint(book_router)
    app.register_blueprint(author_of_book_router)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")
