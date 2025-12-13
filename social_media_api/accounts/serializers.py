# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # Expose necessary fields for registration
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

    def create(self, validated_data):
        # Use create_user for proper password hashing
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Fields to expose for profile viewing/editing
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'followers', 'following')
        read_only_fields = ('followers', 'following') # Followers and following are managed elsewhere