from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    It translates the Book model instance into JSON format for the API response
    and handles deserialization of incoming data.
    """
    class Meta:
        # Specify the model to be serialized
        model = Book
        
        # 'fields = "__all__"' includes all fields from the Book model: 
        # title, author, and publication_date
        fields = '__all__'
        
        # Alternatively, you could list specific fields: 
        # fields = ['id', 'title', 'author', 'publication_date']