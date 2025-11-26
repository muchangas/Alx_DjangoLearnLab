from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AuthorViewSet,
    BookListCreate,
    BookDetail,
    BookUpdate,
    BookDelete
)

# Use DefaultRouter for AuthorViewSet
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)

# =========================================================================
# Explicit URL Patterns for Book Generic Views
# =========================================================================
urlpatterns = [
    # 1. Author ViewSet (Automatic Router)
    path('', include(router.urls)),

    # 2. Book Generic Views (Manual Configuration)
    # List (GET) and Create (POST)
    path('books/generic/', BookListCreate.as_view(), name='book-list-create'),

    # Detail (GET)
    path('books/generic/<int:pk>/', BookDetail.as_view(), name='book-detail'),

    # Update (PUT/PATCH)
    path('books/generic/<int:pk>/update/', BookUpdate.as_view(), name='book-update'),

    # Delete (DELETE)
    path('books/generic/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),
]