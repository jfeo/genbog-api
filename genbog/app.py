"""GenBog Flask Application

This module contains the functionality to set up the GenBog Flask application.

The module contains the function:

    * create_app - sets up the routing, and more for the Flask application
"""

from flask import Flask, request, jsonify, json
from werkzeug.exceptions import InternalServerError, HTTPException

from .repository import InMemoryRepository
from .util import ISBNConverter, parse_isbn, ApplicationError


def create_app():
    """Creates a Flask app, and sets up routes, converters, and error
    handlers.

    returns: The created Flask application object.
    """
    app = Flask(__name__)
    app.url_map.converters['isbn'] = ISBNConverter

    repository = InMemoryRepository()

    @app.route("/books/<isbn:isbn>", methods=["GET"])
    def get_book(isbn):
        return jsonify({"isbn": isbn, "count": repository.count(isbn)}), 200

    @app.route("/books/<isbn:isbn>", methods=["POST"])
    def post_book(isbn):
        repository.add(isbn)
        return jsonify({"isbn": isbn, "count": repository.count(isbn)})

    @app.route("/books/<isbn:isbn>", methods=["DELETE"])
    def delete_book(isbn):
        repository.remove(isbn)
        return jsonify({"isbn": isbn, "count": repository.count(isbn)}), 200

    @app.route("/books", methods=["GET"])
    def get_books():
        return jsonify([{
            "isbn": isbn,
            "count": count
        } for isbn, count in repository.list_all()]), 200

    @app.route("/books", methods=["POST"])
    def post_books():
        request_isbns = request.get_json(force=False, silent=False, cache=False)
        for isbn in list(map(parse_isbn, request_isbns)):
            repository.add(isbn)
        return jsonify([{
            "isbn": isbn,
            "count": repository.count(isbn)
        } for isbn in request_isbns]), 200

    @app.errorhandler(InternalServerError)
    def handle_500(exception):
        if not hasattr(exception, 'original_exception'):
            return jsonify({"error": "An internal server error occured"}), 500

        if isinstance(exception.original_exception, ApplicationError):
            return jsonify(exception.original_exception.data), 400

        return jsonify({"error": repr(exception.original_exception)}), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(exception):
        response = exception.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": exception.code,
            "name": exception.name,
            "description": exception.description,
        })
        response.content_type = "application/json"
        return response

    return app
