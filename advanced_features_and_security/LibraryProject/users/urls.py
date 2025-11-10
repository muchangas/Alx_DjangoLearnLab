# relationship_app/urls.py

from django.urls import path
from . import views
from .views import LibraryDetailView
from .views import list_books
"views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="
"add_book/", "edit_book/", "delete_book"
# Define the app's namespace for use in templates (e.g., {% url 'relationship_app:books' %})
app_name = 'relationship_app'

urlpatterns = [
    # Function-based View (FBV): Lists all books at the /books/ path
    path('books/', views.list_all_books, name='book_list'),
    
    # Class-based View (CBV): Displays details for a specific library at /library/1/
    # Uses the primary key (pk) from the URL to fetch the specific Library object
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
