from django.contrib import admin
from .models import Author, Book

# =========================================================================
# Admin Configuration
# =========================================================================

# Register models to make them available in the Django Admin interface.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for the Author model."""
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for the Book model."""
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author__name')
    # Adding 'author' to list_select_related optimizes database queries
    list_select_related = ('author',)