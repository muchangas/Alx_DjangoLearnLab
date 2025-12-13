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
        
        # The authenticated user performing the action
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

        # Add the relationship: current_user follows user_to_follow
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