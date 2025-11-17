# relationship_app/views.py
"relationship_app/list_books.html", "Book.objects.all()"
from django.shortcuts import render
from django.views.generic import DetailView
# 🎯 CORRECTED IMPORT: Explicitly including 'Library' in the import statement
from .models import Book, Library 

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

# relationship_app/views.py (Additions for RBAC)

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test # <-- Import the decorator

# Import all models
from .models import Book, Library, UserProfile 

# --- Existing Views (List all books, LibraryDetailView, register) remain here ---
# ...
# Your previous views (list_all_books, LibraryDetailView, register) go here
# ...


# --- RBAC Check Functions ---
def is_admin(user):
    """Checks if a user has the 'Admin' role."""
    return user.is_authenticated and user.profile.role == 'Admin'

def is_librarian(user):
    """Checks if a user has the 'Librarian' role."""
    return user.is_authenticated and user.profile.role == 'Librarian'

def is_member(user):
    """Checks if a user has the 'Member' role."""
    # This check is often just for logged-in status if 'Member' is the base role
    return user.is_authenticated and user.profile.role == 'Member'


# --- RBAC Views ---

@user_passes_test(is_admin, login_url='/relationships/login/')
def admin_view(request):
    """View accessible only by Admin users."""
    context = {'user_role': request.user.profile.role}
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian, login_url='/relationships/login/')
def librarian_view(request):
    """View accessible only by Librarian users."""
    context = {'user_role': request.user.profile.role}
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member, login_url='/relationships/login/')
def member_view(request):
    """View accessible only by Member users."""
    context = {'user_role': request.user.profile.role}
    return render(request, 'relationship_app/member_view.html', context)