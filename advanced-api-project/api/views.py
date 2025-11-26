from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# =========================================================================
# View Definitions - Author (Using ModelViewSet for Simplicity)
# =========================================================================

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Author instances.
    Kept as ModelViewSet to demonstrate the power of automatic routing.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # Read-only for unauthenticated users, fully editable for staff/superusers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# =========================================================================
# View Definitions - Book (Using Custom Generic Views for Granularity)
# This demonstrates precise control over permissions and functionality for
# each type of CRUD operation.
# =========================================================================

class BookListCreate(generics.ListViewCreateView):
    """
    Book List View (GET /api/books/generic/)
    Book Create View (POST /api/books/generic/)

    Configuration:
    - queryset: Defines the set of books to retrieve.
    - serializer_class: Specifies the serializer for data conversion and validation.
    - permission_classes:
        - List (GET) is allowed for any user (IsAuthenticatedOrReadOnly).
        - Create (POST) requires the user to be authenticated.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Customization Example (Optional):
    # def perform_create(self, serializer):
    #     # Example hook: automatically set the author to the current logged-in user,
    #     # assuming the Author model was linked to the User model.
    #     # serializer.save(author=self.request.user.author_profile)
    #     serializer.save()


class BookDetail(generics.DetailView):
    """
    Book Detail View (GET /api/books/generic/<pk>/)

    Configuration:
    - retrieve method is read-only.
    - Permissions are set to allow any user to read a specific book (AllowAny).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookUpdate(generics.UpdateView):
    """
    Book Update View (PUT/PATCH /api/books/generic/<pk>/update/)

    Configuration:
    - Only authenticated users can perform updates.
    - `UpdateAPIView` handles both PUT (full replacement) and PATCH (partial update).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Restrict to authenticated users for writing operations
    permission_classes = [permissions.IsAuthenticated]

    # Customization Example: You could override perform_update here for side effects
    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     # Send a notification after a successful update
    #     # print(f"Book {instance.title} updated successfully.")


class BookDelete(generics.DeleteView):
    """
    Book Delete View (DELETE /api/books/generic/<pk>/delete/)

    Configuration:
    - Only authenticated users can perform deletions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Restrict to authenticated users for deletion
    permission_classes = [permissions.IsAuthenticated]