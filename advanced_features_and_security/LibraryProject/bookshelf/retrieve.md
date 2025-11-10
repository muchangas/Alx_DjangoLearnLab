# Retrieve Operation

**Command:** Retrieve and display all attributes of the book with the title "1984".

## Python Command Used
```python
from bookshelf.models import Book
retrieved_book = Book.objects.get(title="1984")
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Year: {retrieved_book.publication_year}")
