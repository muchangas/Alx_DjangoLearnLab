# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# --- Custom Admin Model (Step 4) ---

class CustomUserAdmin(UserAdmin):
    """
    Define custom admin forms and fields for the CustomUser model.
    """
    
    # Fields to display in the user list view
    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo',)
    
    # Fields to use when creating a new user via the admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # Fields to use when changing an existing user via the admin
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info (Custom)', {'fields': ('date_of_birth', 'profile_photo',)}),
    )

# Unregister the default User model (if the app was named 'auth') 
# and register the custom one. Since we're in the 'users' app, 
# we only need to register the custom one.
admin.site.register(CustomUser, CustomUserAdmin)