# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Additional fields
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Many-to-Many relationship for followers
    # 'self' refers to this model (CustomUser)
    # symmetrical=False allows user A to follow user B without B automatically following A
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', # Renames the reverse relation from follower to following
        blank=True
    )

    def __str__(self):
        return self.username