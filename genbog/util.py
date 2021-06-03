"""This module contains utility methods for the Flask application.

The module exports the following classes:

    * ApplicationError - an Exception class that represents errors that should
                         be displayed to API users.
    * ISBNError - a sublcass of ApplicationError raised when an invalid ISBN
                  code is encountered.
    * ISBNConverter - a subclass of workzeug.routing.BaseConverter to parse
                      ISBN codes from URL variables.

The module exports the following methods:

    * parse_isbn - raises ISBNErrors for invalid ISBN codes.
"""

from werkzeug.routing import BaseConverter


def parse_isbn(isbn: str):
    """Raise an ISBNError if the given ISBN code is invalid.

    Returns: the valid ISBN codes given to it."""
    if len(isbn) == 13 and isbn.isdigit():
        return isbn
    raise ISBNError(isbn)


class ApplicationError(Exception):
    """An Exception subclass that represent errors that should be displayed by
    the API to users, to indicate what is wrong."""
    def __init__(self, msg, **data):
        super().__init__(msg)
        self.data = data
        self.data.update({"error": msg})


class ISBNError(ApplicationError):
    """An Error that subclasses the ApplicationError specific to invalid ISBN
    codes."""
    def __init__(self, isbn):
        super().__init__(f"Value '{isbn}' is not a valid ISBN.", isbn=isbn)


class ISBNConverter(BaseConverter):
    """A URL converter for ISBN values, that raises ISBNErrors on invalid
    ISBN codes."""

    def to_python(self, value):
        return parse_isbn(value)

    def to_url(self, value):
        return value
