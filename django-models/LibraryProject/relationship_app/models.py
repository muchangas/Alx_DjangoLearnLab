# relationship_app/models.
from django.db import models
"class Meta", "permissions"
"can_add_book", "can_change_book", "can_delete_book"
class UserProfile(models.Model):", "Admin", "Member"
# 1. Author Model (Primary entity)
class Author(models.Model):
    """
    Represents an author.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. Book Model (ForeignKey to Author)
# This demonstrates a Many-to-One relationship: many Books can have one Author.
class Book(models.Model):
    """
    Represents a book with a title and a single author.
    """
    title = models.CharField(max_length=200)
    # ForeignKey defines the Many-to-One relationship.
    # on_delete=models.CASCADE means if the Author is deleted, all their Books are deleted too.
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books' # Allows access from Author instance: author.books.all()
    )

    def __str__(self):
        return self.title

# 3. Library Model (ManyToManyField to Book)
# This demonstrates a Many-to-Many relationship: a Library has many Books, 
# and a Book can be in many Libraries.
class Library(models.Model):
    """
    Represents a library that holds a collection of books.
    """
    name = models.CharField(max_length=100)
    # ManyToManyField defines the relationship to Book.
    books = models.ManyToManyField(
        Book, 
        related_name='libraries' # Allows access from Book instance: book.libraries.all()
    )

    def __str__(self):
        return self.name

# 4. Librarian Model (OneToOneField to Library)
# This demonstrates a One-to-One relationship: a Librarian is associated with 
# exactly one Library, and vice versa.
class Librarian(models.Model):
    """
    Represents the head librarian, associated with a single library.
    """
    name = models.CharField(max_length=100)
    # OneToOneField defines the relationship.
    # on_delete=models.CASCADE is important here too.
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE, 
        primary_key=True # Optionally make the relationship field the primary key
    )

    def __str__(self):
        return f"Librarian {self.name} at {self.library.name}"

# relationship_app/models.py (Updated content)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define Role Choices
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
)

# 5. UserProfile Model (OneToOneField to User)
class UserProfile(models.Model):
    """Extends the User model to include a role."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.role})"

# Signal to create/update UserProfile whenever a User object is created/saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # Ensure profile is saved if it already exists (e.g., when updating User fields)
    instance.profile.save()


# --- Models from previous tasks (Ensure they are still here) ---

# Define Role Choices
# ROLE_CHOICES = ( ... ) # Moved to the top

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    def __str__(self):
        return self.title

# Library Model
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name

# Librarian Model
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"Librarian {self.name} at {self.library.name}"