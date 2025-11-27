import json
import logging
from pathlib import Path
from .book import Book

class LibraryInventory:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_books()
        logging.info(f"Book added: {title}")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return [b for b in self.books if b.isbn == isbn]

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        for book in self.books:
            print(book)

    def save_books(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except IOError as e:
            logging.error(f"Failed to save inventory: {e}")

    def load_books(self):
        path = Path(self.filename)
        if not path.exists():
            logging.info("No inventory file found. Starting fresh.")
            return

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading inventory: {e}")
