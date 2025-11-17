from django.db import models
"class CustomUser(AbstractUser):", "date_of_birth", "profile_photo"
"class CustomUserManager(BaseUserManager):", "create_user", "create_superuser"
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
# bookshelf/models.py

from django.db import models
from django.conf import settings # Needed if using AUTH_USER_MODEL

class Book(models.Model):
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    published_date = models.DateField()
    
    # Assuming CustomUser from the previous task
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books_created'
    )

    class Meta:
        # Step 1: Define Custom Permissions
        permissions = [
            ("can_view", "Can view book details"),
            ("can_create", "Can create a new book"),
            ("can_edit", "Can edit existing book details"),
            ("can_delete", "Can delete a book entry"),
        ]
        
    def __str__(self):
        return self.title

# After adding these, run: python manage.py makemigrations bookshelf
# And then: python manage.py migrate