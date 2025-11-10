# relationship_app/query_samples.py

# Instructions: Run this content inside the Django shell: $ python manage.py shell

from relationship_app.models import Author, Book, Library, Librarian

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
    Librarian.objects.create(name="Mr. Smith", library=library_central)
    Librarian.objects.create(name="Ms. Johnson", library=library_branch)

    print("Data setup complete.")

def sample_queries():
    """Demonstrates queries for the three relationship types."""
    print("\n--- Running Sample Queries ---")

# --- QUERY 1: ForeignKey Relationship (Query all books by a specific author) ---
    author_name = "George Orwell"
    print(f"\n[QUERY 1] Books by {author_name} (ForeignKey - Explicit Filter):")
    try:
        author_instance = Author.objects.get(name=author_name)
        
        # CORRECTED QUERY: Uses explicit filter as requested
        # objects.filter(author=author) where 'author' is the Author instance
        orwell_books = Book.objects.filter(author=author_instance) 
        
        for book in orwell_books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")


    # --- QUERY 2: ManyToMany Relationship (List all books in a library) ---
    library_name = "Central City Library"
    print(f"\n[QUERY 2] Books in {library_name} (ManyToMany):")
    try:
        # CORRECTED: Use variable for lookup: Library.objects.get(name=library_name)
        central_library = Library.objects.get(name=library_name) 
        # Access the ManyToMany field directly
        central_books = central_library.books.all() 
        for book in central_books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")


# --- QUERY 3: OneToOne Relationship (Retrieve the librarian for a library) ---
    library_name = "North Branch Library"
    print(f"\n[QUERY 3] Librarian for {library_name} (OneToOne - Direct Query):")
    try:
        # Step 1: Find the target Library instance (required for the direct lookup)
        branch_library_instance = Library.objects.get(name=library_name)

        # Step 2: Use the direct lookup on the Librarian model
        # CORRECTED QUERY: Librarian.objects.get(library=instance)
        branch_librarian = Librarian.objects.get(library=branch_library_instance)
        
        print(f"- Librarian Name: {branch_librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"Librarian not found associated with '{library_name}'.")

    print("\n--- Queries finished ---")

# Execute setup and queries
setup_data()
sample_queries()