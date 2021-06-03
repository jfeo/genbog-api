from werkzeug.routing import BaseConverter


def parse_isbn(isbn: str):
    if len(isbn) == 13 and isbn.isdigit():
        return isbn
    raise ISBNError(isbn)


class ApplicationError(Exception):

    def __init__(self, msg, **data):
        super().__init__(msg)
        self.data = data
        self.data.update({"error": msg})


class ISBNError(ApplicationError):

    def __init__(self, isbn):
        super().__init__(f"Value '{isbn}' is not a valid ISBN.", isbn=isbn)


class ISBNConverter(BaseConverter):

    def to_python(self, value):
        return parse_isbn(value)

    def to_url(self, value):
        return value
