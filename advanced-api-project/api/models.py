from django.db import models

# =========================================================================
# Model Definitions
# =========================================================================

class Author(models.Model):
    """
    Model representing an Author. This model is the 'one' side of the
    one-to-many relationship with the Book model.
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a Book. This model is the 'many' side of the
    one-to-many relationship, linking back to the Author model via a ForeignKey.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    # ForeignKey links the Book to an Author. related_name='books' is crucial
    # for fetching all books associated with an author instance (Author.books.all()).
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        unique_together = ('title', 'author') # Ensures an author doesn't have two books with the exact same title
        ordering = ['-publication_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.publication_year})"