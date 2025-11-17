from django.urls import path
from .views import BookList

# Define the app name for namespace separation (good practice)
app_name = 'api'

urlpatterns = [
    # Maps GET requests to /api/books/ to the BookList view
    path('books/', BookList.as_view(), name='book-list'),
]