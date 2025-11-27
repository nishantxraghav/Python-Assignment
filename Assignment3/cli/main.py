import sys
import os
import logging

# Ensure we can import from library_manager folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_manager.inventory import LibraryInventory

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    lib = LibraryInventory()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Search Book")
        print("5. View All")
        print("6. Exit")
        
        choice = input("Enter choice: ")

        try:
            if choice == '1':
                t = input("Title: ")
                a = input("Author: ")
                i = input("ISBN: ")
                lib.add_book(t, a, i)
                print("Book added successfully.")

            elif choice == '2':
                isbn = input("Enter ISBN to issue: ")
                results = lib.search_by_isbn(isbn)
                if results:
                    if results[0].issue():
                        lib.save_books()
                        print("Book issued.")
                    else:
                        print("Book is already issued.")
                else:
                    print("Book not found.")

            elif choice == '3':
                isbn = input("Enter ISBN to return: ")
                results = lib.search_by_isbn(isbn)
                if results:
                    results[0].return_book()
                    lib.save_books()
                    print("Book returned.")
                else:
                    print("Book not found.")

            elif choice == '4':
                term = input("Enter Title or ISBN to search: ")
                # Simple check to decide which search to run
                results = lib.search_by_isbn(term) if term.isdigit() else lib.search_by_title(term)
                for b in results:
                    print(b)

            elif choice == '5':
                lib.display_all()

            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
