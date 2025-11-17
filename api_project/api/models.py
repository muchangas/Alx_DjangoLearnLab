from django.db import models

class Book(models.Model):
    """
    A simple model to represent a book.
    This model will be exposed via a Django REST Framework API.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
