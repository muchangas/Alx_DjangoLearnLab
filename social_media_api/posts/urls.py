# posts/urls.py (Alternative without drf-nested-routers)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

# Manually define comment routes, assuming PostViewSet uses lookup='pk'
urlpatterns = [
    path('', include(router.urls)),
    
    # List and Create comments for a specific post
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments-list'),
    
    # Retrieve, Update, Destroy a specific comment
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-comments-detail'),
]