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
    path('feed/', UserFeedView.as_view(), name='user_feed'), # <-- ADDED
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments-list'),
    
    # Retrieve, Update, Destroy a specific comment
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-comments-detail'),
]
# posts/urls.py (Update)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserFeedView, LikePostView # <--- Import LikePostView
# ...

urlpatterns = [
    path('feed/', UserFeedView.as_view(), name='user_feed'), 

    # New Like/Unlike Route (Toggles like status)
    # The 'unlike' functionality is built into the POST method of LikePostView
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post_like_toggle'),

    # Existing Post and Comment Routes "<int:pk>/unlike/"
    path('', include(router.urls)), 
    # ... nested comment routes ...
]