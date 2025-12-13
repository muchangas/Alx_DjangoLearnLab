# posts/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# --- Custom Pagination ---

class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- Post ViewSet ---

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    
    # Filtering and Searching
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author__username', 'created_at']
    search_fields = ['title', 'content'] # Fields to search against
    
    # Logic to automatically set the author to the currently logged-in user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Comment ViewSet ---

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    # No pagination on comments, but we should restrict comments to a specific post
    # We will filter the queryset based on the URL provided in the router setup
    
    # Set the author and post automatically
    def perform_create(self, serializer):
        # Assumes the URL is structured like /posts/{post_pk}/comments/
        post_pk = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        
        # Save the comment with the current user as author and the post from the URL
        serializer.save(author=self.request.user, post=post)

    # Override get_queryset to filter comments by post_pk from the URL
    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return self.queryset.filter(post__pk=post_pk)
        return self.queryset