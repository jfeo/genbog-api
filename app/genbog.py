from flask import Flask, request, jsonify

app = Flask(__name__)


def validate_isbn(isbn: str):
    return len(isbn) == 13 and isbn.isdigit()


isbns = {}


def add_book(isbn):
    if isbn in isbns:
        isbns[isbn] += 1
    else:
        isbns[isbn] = 1


def remove_book(isbn):
    if isbn in isbns:
        if isbns[isbn] == 1:
            del isbns[isbn]
        else:
            isbns[isbn] -= 1


@app.route("/books/<isbn>", methods=["GET", "POST", "DELETE"])
def book(isbn):
    if not validate_isbn(isbn):
        return jsonify({"error": "Invalid ISBN"}), 400
    if request.method == "GET":
        if isbn in isbns:
            return jsonify({"isbn": isbn, "count": isbns[isbn]}), 200
        else:
            return jsonify({"error": "ISBN not found", "isbn": isbn}), 404
    elif request.method == "POST":
        add_book(isbn)
        return jsonify({"isbn": isbn, "count": isbns[isbn]})
    elif request.method == "DELETE":
        remove_book(isbn)
        return jsonify({"isbn": isbn, "count": isbns[isbn] if isbn in isbns else 0})
    else:
        return jsonify({"error": "Not yet implemented"}), 500


@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        bs = [{"isbn": isbn, "count": count} for isbn, count in isbns.items()]
        return jsonify(bs), 200
    elif request.method == "POST":
        request_isbns = request.get_json(force=False, silent=False, cache=False)
        for isbn in request_isbns:
            if not validate_isbn(isbn):
                return jsonify({"error": "Invalid ISBN", "isbn": isbn}), 400
        for isbn in request_isbns:
            add_book(isbn)
        return jsonify([{"isbn": isbn, "count": isbns[isbn]}
                        for isbn in request_isbns]), 200


@app.errorhandler(404)
def handle_404(err):
    return 404, "Not Found"
