# accounts/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token # <-- HERE IS WHERE TOKEN IS IMPORTED
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 1. User object is created by the serializer's create() method
        user = serializer.save()

        # 2. Token creation is handled in the View
        token, created = Token.objects.get_or_create(user=user) # <-- HERE IS WHERE TOKEN IS CREATED/RETRIEVED

        return Response({
            "user_id": user.pk,
            "username": user.username,
            "token": token.key, # Return the generated token
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user using Django's built-in system
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Token retrieval is handled in the View
            token, created = Token.objects.get_or_create(user=user) # <-- HERE IS WHERE TOKEN IS RETRIEVED

            return Response({
                "user_id": user.pk,
                "username": user.username,
                "token": token.key, 
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# UserProfileView remains the same
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # The user to be followed
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        
        # The authenticated user performing the action Post.objects.filter(author__in=following_users).order_by", "permissions.IsAuthenticated"
        current_user = request.user

        if current_user == user_to_follow:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the user is already following
        if current_user.following.filter(pk=user_to_follow.pk).exists():
            return Response(
                {"detail": f"You are already following {user_to_follow.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add the relationship:Post.objects.filter(author__in=following_users).order_by", "permissions.IsAuthenticated" generics.GenericAPIView, permissions.IsAuthenticated current_user follows user_to_follow
        # 'following' is the reverse relationship manager of the 'followers' M2M field
        current_user.following.add(user_to_follow)
        
        return Response(
            {"detail": f"Successfully followed {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # The user to be unfollowed
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        
        current_user = request.user

        if current_user == user_to_unfollow:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user is actually following
        if not current_user.following.filter(pk=user_to_unfollow.pk).exists():
             return Response(
                {"detail": f"You are not following {user_to_unfollow.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove the relationship
        current_user.following.remove(user_to_unfollow)

        return Response(
            {"detail": f"Successfully unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )
    
    # posts/views.py

from rest_framework import viewsets
from rest_framework.generics import ListAPIView # <--- Needed for UserFeedView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated # <--- IsAuthenticated is needed for the Feed
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
    # ... (content remains the same) ...
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author__username', 'created_at']
    search_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Comment ViewSet ---
class CommentViewSet(viewsets.ModelViewSet):
    # ... (content remains the same) ...
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return self.queryset.filter(post__pk=post_pk)
        return self.queryset

# --- User Feed View ---
class UserFeedView(ListAPIView):
    """
    Returns a list of posts from all users that the current user is following,
    ordered by creation date (newest first).
    """
    serializer_class = PostSerializer
    # CORRECT: Permissions are mandatory for a private feed
    permission_classes = [IsAuthenticated] 
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user
        
        # 1. Get the list of followed users
        following_users = user.following.all()
        
        # 2. Filter, optimize, and order the posts
        # CORRECT: Using .filter(author__in=...) and .order_by('-created_at')
        queryset = Post.objects.filter(
            author__in=following_users
        ).select_related('author').order_by('-created_at')
        
        return 

# accounts/views.py (Modify FollowUserView)

from notifications.tasks import notify_user_followed # <--- ADD IMPORT

# ... Existing FollowUserView class ...

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # ... (Existing follow logic and checks) ...
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        current_user = request.user
        
        # ... (Existing checks for self-follow and already following) ...

        # Add the relationship: current_user follows user_to_follow
        current_user.following.add(user_to_follow)
        
        # New: Generate Notification
        notify_user_followed(follower=current_user, followed=user_to_follow)

        return Response(
            {"detail": f"Successfully followed {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )

# UnfollowUserView remains the same (no notification needed for unfollow)