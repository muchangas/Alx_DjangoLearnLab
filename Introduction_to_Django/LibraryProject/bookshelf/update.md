# Update Operation

**Command:** Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

## Python Command Used
```python
from bookshelf.models import Book
book_to_update = Book.objects.get(title="1984")
# The attribute being updated is book_to_update.title
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
print(book_to_update.title)
