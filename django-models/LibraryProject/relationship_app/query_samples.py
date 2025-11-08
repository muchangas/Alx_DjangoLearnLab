# relationship_app/query_samples.py

# To run this script, you must first set up the Django environment:
# 1. In your project's main directory, open the Django shell:
#    $ python manage.py shell
# 2. Paste the contents of this file into the shell and press Enter.

from relationship_app.models import Author, Book, Library, Librarian
from django.db.models import Count

def setup_data():
    """Sets up sample data for querying."""
    print("--- Setting up sample data ---")
    
    # 1. Create Authors
    author1 = Author.objects.create(name="Jane Austen")
    author2 = Author.objects.create(name="George Orwell")

    # 2. Create Books (ForeignKey)
    book1 = Book.objects.create(title="Pride and Prejudice", author=author1)
    book2 = Book.objects.create(title="1984", author=author2)
    book3 = Book.objects.create(title="Animal Farm", author=author2)

    # 3. Create Libraries
    library_central = Library.objects.create(name="Central City Library")
    library_branch = Library.objects.create(name="North Branch Library")

    # 4. Add Books to Libraries (ManyToMany)
    library_central.books.add(book1, book2, book3)
    library_branch.books.add(book1)
    
    # 5. Create Librarians (OneToOne)
    librarian_central = Librarian.objects.create(name="Mr. Smith", library=library_central)
    librarian_branch = Librarian.objects.create(name="Ms. Johnson", library=library_branch)

    print("Data setup complete.")

def sample_queries():
    """Demonstrates queries for the three relationship types."""
    print("\n--- Running Sample Queries ---")

    # --- QUERY 1: ForeignKey Relationship ---
    # Query all books by a specific author (using the related_name 'books')
    print("\n[QUERY 1] Books by George Orwell (Author ID 2):")
    try:
        orwell = Author.objects.get(name="George Orwell")
        # Use the reverse relationship manager: author_instance.books.all()
        orwell_books = orwell.books.all()
        for book in orwell_books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print("Author 'George Orwell' not found.")


    # --- QUERY 2: ManyToMany Relationship ---
    # List all books in a library
    print("\n[QUERY 2] Books in Central City Library:")
    try:
        central_library = Library.objects.get(name="Central City Library")
        # Access the ManyToMany field directly
        central_books = central_library.books.all() 
        for book in central_books:
            print(f"- {book.title} (Author: {book.author.name})")
    except Library.DoesNotExist:
        print("Library 'Central City Library' not found.")


    # --- QUERY 3: OneToOne Relationship ---
    # Retrieve the librarian for a library (using the default reverse accessor 'librarian')
    print("\n[QUERY 3] Librarian for North Branch Library:")
    try:
        branch_library = Library.objects.get(name="North Branch Library")
        # Access the reverse OneToOne relationship: library_instance.model_name_lowercase
        branch_librarian = branch_library.librarian
        print(f"- Librarian Name: {branch_librarian.name}")
    except Library.DoesNotExist:
        print("Library 'North Branch Library' not found.")
    except Librarian.DoesNotExist:
        print("Librarian not found for North Branch Library.")

    print("\n--- Queries finished ---")

# Run the setup and queries
setup_data()
sample_queries()