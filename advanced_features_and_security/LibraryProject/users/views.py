# relationship_app/views.py
"relationship_app/list_books.html", "Book.objects.all()"
from django.contrib.auth.decorators import permission_required", "relationship_app.can_add_book", "relationship_app.can_change_book", "relationship_app.can_delete_book
from django.shortcuts import render
from django.views.generic.detail import DetailView
# 🎯 CORRECTED IMPORT: Explicitly including 'Library' in the import statement
from .models import Book, Library 
from .models import Library
from django.contrib.auth import login", "from django.contrib.auth.forms import UserCreationForm
# --- 1. Function-based View (FBV) ---
def list_all_books(request):
    """
    Function-based view to list all books.
    """
    # Uses the basic Book.objects.all() query structure
    books = Book.objects.all().order_by('title')
    
    context = {
        'books': books
    }
    
    # Uses the full app-prefixed template path
    return render(request, 'relationship_app/list_books.html', context)


# --- 2. Class-based View (CBV) ---
class LibraryDetailView(DetailView):
    """
    Class-based view (DetailView) to display a specific library's details.
    """
    # model requires the Library model, which is now explicitly imported
    model = Library
    
    # 🎯 CORRECTED TEMPLATE PATH: Uses 'relationship_app/library_detail.html'
    template_name = 'relationship_app/library_detail.html'
    
    context_object_name = 'library'
    
    # Ensures efficient fetching of ManyToMany data for the template
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
