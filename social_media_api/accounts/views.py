# accounts/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Token generation upon successful registration
        token, created = Token.objects.get_or_create(user=user)

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

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            # We don't necessarily call Django's login, but we retrieve the token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "user_id": user.pk,
                "username": user.username,
                "token": token.key, # Return the existing or newly created token
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        else:
            # Login failed
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure the user can only view/edit their own profile
        return self.request.user

    # You don't need to override 'get' and 'put/patch' for simple RetrieveUpdate
    # but the get_object ensures the correct user is returned.
