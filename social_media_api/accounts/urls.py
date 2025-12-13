# accounts/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    # /register/ - User registration
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    
    # /login/ - User login and token retrieval
    path('login/', UserLoginView.as_view(), name='user_login'),
    
    # /profile/ - View/Edit authenticated user's profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='user_unfollow'),
]