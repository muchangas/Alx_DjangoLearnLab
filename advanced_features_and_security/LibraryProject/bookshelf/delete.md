# Delete Operation "book.delete"

**Command:** Delete the book you created and confirm the deletion by trying to retrieve all books again.

## Python Command Used
```python
from bookshelf.models import Book # Required import for shell interaction
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")
# Delete the instance using book_to_delete.delete()
book_to_delete.delete() 
all_books = Book.objects.all()
print(all_books)


