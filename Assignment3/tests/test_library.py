import unittest
import os
import sys
import json

# Add parent directory to path so we can import library_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_manager.book import Book
from library_manager.inventory import LibraryInventory

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        """Runs before every test: Setup a temporary test database."""
        self.test_db = "test_data.json"
        self.lib = LibraryInventory(filename=self.test_db)

    def tearDown(self):
        """Runs after every test: Clean up the temporary file."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_book_creation(self):
        """Test if a book is created with correct attributes."""
        book = Book("Python 101", "Guido", "12345")
        self.assertEqual(book.title, "Python 101")
        self.assertEqual(book.status, "available")

    def test_issue_and_return(self):
        """Test issuing and returning a book."""
        book = Book("Test Book", "Author", "000")
        
        # Issue the book
        self.assertTrue(book.issue())
        self.assertEqual(book.status, "issued")
        
        # Try issuing again
        self.assertFalse(book.issue())
        
        # Return the book
        book.return_book()
        self.assertEqual(book.status, "available")

    def test_add_and_search_inventory(self):
        """Test adding a book to inventory and searching for it."""
        self.lib.add_book("Clean Code", "Uncle Bob", "999")
        
        # Search by Title
        results = self.lib.search_by_title("Clean")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].isbn, "999")

        # Search by ISBN
        results_isbn = self.lib.search_by_isbn("999")
        self.assertEqual(len(results_isbn), 1)

    def test_persistence(self):
        """Test if data is actually saved to the JSON file."""
        self.lib.add_book("Persistent Book", "Author X", "111")
        
        # Force reload from file by creating a new instance
        new_lib_instance = LibraryInventory(filename=self.test_db)
        results = new_lib_instance.search_by_isbn("111")
        
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0].title, "Persistent Book")

if __name__ == "__main__":
    unittest.main()
