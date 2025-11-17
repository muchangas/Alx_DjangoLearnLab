from django.contrib import admin
from .models import Book

# Custom ModelAdmin class for the Book model
class BookAdmin(admin.ModelAdmin):
    """
    Customizes the appearance and functionality of the Book model in the Django admin.
    """
    # 1. Customize list view columns
    list_display = ('title', 'author', 'publication_year')

    # 2. Configure list filters (sidebar)
    list_filter = ('publication_year', 'author')

    # 3. Enable search capabilities
    search_fields = ('title', 'author')

    # Make the title field a link to the detail page (improves usability)
    list_display_links = ('title',)


# Register the Book model with the custom BookAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)
