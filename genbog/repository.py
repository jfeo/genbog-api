"""This module contains functionality related to data repositories for the
application.

The module contains the following classes:

    * InMemoryRepository
"""


class InMemoryRepository:
    """Implements a simple in-memory repository for ISBN data."""

    def __init__(self):
        self.isbns = {}

    def has(self, isbn):
        """Check if the repository has the given isbn code.

        Arguments:
            isbn - an ISBN code.

        Returns: true if isbn is contained in the repository."""
        return isbn in self.isbns

    def count(self, isbn):
        """Count the number of occurences of the given ISBN code in the
        repository.

        Arguments:
            isbn - an ISBN code.

        Returns: an integer representing the number of occurences of this ISBN
                 in the repository."""
        if isbn in self.isbns:
            return self.isbns[isbn]

        return 0

    def add(self, isbn):
        """Add an ISBN to the repository.

        Arguments:
            isbn - an ISBN code."""
        if isbn in self.isbns:
            self.isbns[isbn] += 1
        else:
            self.isbns[isbn] = 1

    def list_all(self):
        """Returns all ISBN codes and their associated counts as a list.

        Returns: a list of tuples (isbn, count)."""
        return self.isbns.items()

    def remove(self, isbn):
        """Removes an occurences of an ISBN code from the repository. If the
        ISBN is not in the repository, nothing happens.

        Arguments:
            isbn - an ISBN code."""
        if isbn in self.isbns:
            if self.isbns[isbn] == 1:
                del self.isbns[isbn]
            else:
                self.isbns[isbn] -= 1
