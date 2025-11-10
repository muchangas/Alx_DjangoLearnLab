# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- Custom User Manager (Step 3) ---

class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        The required fields (date_of_birth, profile_photo) are handled via extra_fields.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        
        # Ensures date_of_birth is handled, profile_photo is optional here
        if 'date_of_birth' not in extra_fields:
            raise ValueError(_('Users must have a date of birth set'))
            
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        Superusers are always staff, superuser, and active.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # For simplicity in superuser creation, we'll set a default date of birth 
        # if not provided. In a real app, you might prompt for it.
        extra_fields.setdefault('date_of_birth', '2000-01-01')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)

# --- Custom User Model (Step 1) ---

class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser.
    The `username` field is kept but can be made optional or disabled 
    if desired (e.g., if using email-only login).
    """
    # Custom Fields
    date_of_birth = models.DateField(
        _('date of birth'), 
        null=True, 
        blank=True
    )
    profile_photo = models.ImageField(
        _('profile photo'), 
        upload_to='profiles/', 
        null=True, 
        blank=True
    )

    # Use the custom manager
    objects = CustomUserManager()

    # If you want to use 'email' as the primary login field instead of 'username':
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth'] # fields that prompt upon user creation via createsuperuser

    def __str__(self):
        return self.email or self.username or "User ID: {}".format(self.id)