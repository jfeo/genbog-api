from flask import Flask, request, jsonify, json
from werkzeug.exceptions import InternalServerError, HTTPException

from .repository import InMemoryRepository
from .util import ISBNConverter, parse_isbn, ApplicationError


def create_app():
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
    def handle_500(e):
        if not hasattr(e, 'original_exception'):
            return jsonify({"error": "An internal server error occured"}), 500

        if isinstance(e.original_exception, ApplicationError):
            return jsonify(e.original_exception.data), 400

        return jsonify({"error": repr(e.original_exception)}), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
