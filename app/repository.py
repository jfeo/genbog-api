class InMemoryRepository:

    def __init__(self):
        self.isbns = {}

    def has(self, isbn):
        return isbn in self.isbns

    def count(self, isbn):
        if isbn in self.isbns:
            return self.isbns[isbn]
        else:
            return 0

    def add(self, isbn):
        if isbn in self.isbns:
            self.isbns[isbn] += 1
        else:
            self.isbns[isbn] = 1

    def list_all(self):
        return self.isbns.items()

    def remove(self, isbn):
        if isbn in self.isbns:
            if self.isbns[isbn] == 1:
                del self.isbns[isbn]
            else:
                self.isbns[isbn] -= 1

