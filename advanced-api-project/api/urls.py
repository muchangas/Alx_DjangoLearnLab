from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AuthorViewSet, BookViewSet

# Use DefaultRouter to automatically generate URLs for the ViewSets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]