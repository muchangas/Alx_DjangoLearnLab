from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer # Import the serializer created earlier
from django.db.models import QuerySet

class BookList(ListAPIView):
    """
    API view to list all Book instances.
    It uses ListAPIView, which is perfect for read-only endpoints returning a collection.
    """
    
    # 1. Define the queryset: all books from the database
    queryset: QuerySet[Book] = Book.objects.all()
    
    # 2. Define the serializer class to convert models to JSON
    serializer_class = BookSerializer

# Note: For now, this endpoint will return an empty list until you add data.
