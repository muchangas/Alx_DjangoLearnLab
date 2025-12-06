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