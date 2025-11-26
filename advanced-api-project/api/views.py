from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# =========================================================================
# View Definitions
# =========================================================================

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Author instances.
    This provides endpoints for creating, retrieving, updating, and deleting
    Author objects, and showcases the nested Book list in the serialized output.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Book instances.
    This allows direct interaction with books, including applying the
    publication_year validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
