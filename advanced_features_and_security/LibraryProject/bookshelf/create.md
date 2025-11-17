# Create Operation

**Command:** Create a `Book` instance with the title “1984”, author “George Orwell”, and publication year 1949.

## Python Command Used
```python
from bookshelf.models import Book
book1 = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book1)
