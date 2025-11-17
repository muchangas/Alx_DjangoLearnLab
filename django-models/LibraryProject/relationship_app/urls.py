# relationship_app/urls.py

from django.urls import path
from . import views
from .views import LibraryDetailView
from .views import list_books
"views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="
"add_book/", "edit_book/", "delete_book"
# Define the app's namespace for use in templates (e.g., {% url 'relationship_app:books' %})
app_name = 'relationship_app'

urlpatterns = [
    # Function-based View (FBV): Lists all books at the /books/ path
    path('books/', views.list_all_books, name='book_list'),
    
    # Class-based View (CBV): Displays details for a specific library at /library/1/
    # Uses the primary key (pk) from the URL to fetch the specific Library object
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
<<<<<<< HEAD

# relationship_app/urls.py (Additions for RBAC)

from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # --- Existing Views ---
    path('books/', views.list_all_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', auth_views.LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='relationship_app/logout.html'
    ), name='logout'),
    path('register/', views.register, name='register'),
    
    # --- New: Role-Based Access Views (RBAC) ---
    path('admin_dashboard/', views.admin_view, name='admin_view'),
    path('librarian_portal/', views.librarian_view, name='librarian_view'),
    path('member_area/', views.member_view, name='member_view'),
]
=======
>>>>>>> 16f8ac04288589c95000460b2999e96908c08c51
