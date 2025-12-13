# posts/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

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
    
    # No pagination on comments, Post.objects.filter(author__in=following_users).order_by", "permissions.IsAuthenticated but we should restrict comments to a specific post
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

class UserFeedView(ListAPIView):
    """
    Returns a list of posts from all users that the current user is following,
    ordered by creation date (newest first).
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination # Reuse existing pagination

    def get_queryset(self):
        user = self.request.user
        
        # 1. Get the list of users the current user is following (a QuerySet of CustomUser objects)
        following_users = user.following.all()
        
        # 2. Filter posts to include only those where the author is in the 'following_users' list
        # We also use .select_related('author') to optimize database queries.
        queryset = Post.objects.filter(
            author__in=following_users
        ).select_related('author').order_by('-created_at')
        
        return queryset