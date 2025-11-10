# bookshelf/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View

from .models import Book # Assuming you have BookForm defined elsewhere

# --- Functional View Examples using @permission_required ---

# 1. View protected by 'can_create'
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """View to handle new book creation."""
    if request.method == 'POST':
        # form = BookForm(request.POST)
        # if form.is_valid():
        #     book = form.save(commit=False)
        #     book.creator = request.user
        #     book.save()
        return redirect('book_list')
    # else:
    #     form = BookForm()
    # return render(request, 'bookshelf/create_book.html', {'form': form})
    return render(request, 'bookshelf/create_book.html') # Placeholder

# 2. View protected by 'can_edit'
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """View to handle editing an existing book."""
    # book = get_object_or_404(Book, pk=pk)
    # if request.method == 'POST':
    #     form = BookForm(request.POST, instance=book)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('book_detail', pk=pk)
    # else:
    #     form = BookForm(instance=book)
    # return render(request, 'bookshelf/edit_book.html', {'form': form})
    return render(request, 'bookshelf/edit_book.html') # Placeholder

# 3. View protected by 'can_delete'
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """View to handle deleting a book."""
    # book = get_object_or_404(Book, pk=pk)
    # book.delete()
    return redirect('book_list')
    
# --- Class-Based View Example using PermissionRequiredMixin ---

class BookDetailView(PermissionRequiredMixin, View):
    # PermissionRequiredMixin will automatically check for this permission
    permission_required = 'bookshelf.can_view'
    
    # If the user doesn't have the permission, it raises a 403 Forbidden error
    # You can customize this by setting login_url or raise_exception
    raise_exception = True 

    def get(self, request, pk):
        # book = get_object_or_404(Book, pk=pk)
        # return render(request, 'bookshelf/book_detail.html', {'book': book})
        return render(request, 'bookshelf/book_detail.html') # Placeholder

# Note: You need corresponding URLs and templates for these views to function fully.
