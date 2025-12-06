from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's built-in auth views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # Blog Home
    path('', views.post_list, name='post_list'),
    
    # 1. Registration (Custom View)
    path('register/', views.register, name='register'),

    # 2. Login (Built-in View)
    # Using 'path' instead of 're_path' is recommended for simplicity
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    
    # 3. Logout (Built-in View)
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # 4. Profile Management (Custom View)
    path('profile/', views.profile, name='profile'),
    
    # Optional: Password reset URLs using the built-in system
    # path('password-reset/', 
    #     auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), 
    #     name='password_reset'),
    # ... other password reset paths
]

from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView,
    PostDetailView,         
    register, # Existing FBV
    profile, # Existing FBV
    add_comment,
    CommentUpdateView,
    CommentDeleteView,
    PostDeleteView,

)

urlpatterns = [
    # 1. READ (List - Accessible to all)
    path('', PostListView.as_view(), name='post_list'),
    
    # 2. CREATE (Requires Login)
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # 3. READ (Detail - Accessible to all)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    #  4. UPDATE (Requires Login & Author Check)
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),

    # 5. DELETE (Requires Login & Author Check)
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
 
    # 6. CREATE Comment (Function View)
    path('post/<int:pk>/comment/new/', add_comment, name='add_comment'),

    # 7. UPDATE Comment (Class View)
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    
    # 8. DELETE Comment (Class View)
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # --- Authentication URLs (Keep existing) ---
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', profile, name='profile')
]