# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model # Use get_user_model() for safety

# You need the model manager (CustomUser.objects) to call create_user.
# Using get_user_model() is the safest way to get the active user model.
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # This correctly handles the password field for input validation and exclusion from output
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # Fields for registration
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

    def create(self, validated_data):
        # The serializer uses the create_user method provided by Django's AbstractUser/UserManager
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', '')
        )
        # Token creation is handled in the View, not the Serializer's create method
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    # This serializer is used for retrieving and updating existing users
    
    # You can display the count of followers/following instead of the list of IDs
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        # Fields for profile viewing/editing
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 
                  'profile_picture', 'follower_count', 'following_count')
        read_only_fields = ('follower_count', 'following_count')
        
    def get_follower_count(self, obj):
        # obj is the CustomUser instance
        return obj.followers.count()

    def get_following_count(self, obj):
        # 'following' is the related_name we set up in models.py
        return obj.following.count()