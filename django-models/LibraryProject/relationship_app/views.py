# relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library, Author

# --- 1. Function-based View (FBV) ---
def list_all_books(request):
    """
    Function-based view to list all books.
    Renders the list_books.html template.
    """
    # Fetch all books and select related author data to prevent extra queries (select_related)
    books = Book.objects.select_related('author').all().order_by('title')
    
    context = {
        'books': books
    }
    
    return render(request, 'list_books.html', context)


# --- 2. Class-based View (CBV) ---
class LibraryDetailView(DetailView):
    """
    Class-based view (DetailView) to display a specific library's details.
    Uses the library_detail.html template.
    """
    # 1. Specify the model the view will operate on
    model = Library
    
    # 2. Specify the template to be rendered
    template_name = 'library_detail.html'
    
    # 3. Specify the name used in the template context (e.g., {{ library.name }})
    context_object_name = 'library'
    
    # 4. (Optional but recommended) Override get_queryset to prefetch related objects
    def get_queryset(self):
        """
        Ensures the library's books and the books' authors are fetched 
        in a minimal number of queries (prefetch_related).
        """
        return Library.objects.prefetch_related('books__author')
