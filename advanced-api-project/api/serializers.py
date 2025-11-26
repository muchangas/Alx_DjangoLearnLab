from rest_framework import serializers
from .models import Author, Book
from datetime import date

# =========================================================================
# Serializer Definitions
# =========================================================================

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Handles validation to ensure the publication year is not in the future.
    This serializer is used to represent individual Book objects and is also
    nested within the AuthorSerializer to show an author's bibliography.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']

    def validate_publication_year(self, value):
        """
        Custom validation method to check if the publication year is in the past or present.
        The current year is retrieved from the system date.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future. Must be less than or equal to {current_year}.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    This serializer demonstrates nested serialization: it includes the basic
    Author fields (name) and a list of all related Book objects using the
    BookSerializer (many=True).

    Relationship Handling:
    - The `books` field links to the `related_name='books'` defined on the
      ForeignKey in the Book model.
    - Setting `many=True` tells DRF to expect and serialize a list of Book objects.
    - Setting `read_only=True` makes the nested field display-only in GET requests,
      as complex nested writes require custom `create()` or `update()` methods,
      which are omitted here for simplicity in a read-only nested structure.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']