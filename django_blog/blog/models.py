from django.db import models
from django.contrib.auth.models import User

# 

class Post(models.Model):
    """
    A model representing a single blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Auto-sets the date/time when the post is first created
    published_date = models.DateTimeField(auto_now_add=True)
    # ForeignKey creates a one-to-many relationship: One User can write many Posts.
    # on_delete=models.CASCADE means if the User is deleted, their Posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # Orders posts by the newest published_date first
        ordering = ['-published_date']

    def __str__(self):
        """String representation of the Post object."""
        return self.title
    
# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Needed for the Post model's get_absolute_url

# ... (Existing Post model definition) ...
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        # Redirect to the detail view after creating/updating a post
        return reverse('post_detail', kwargs={'pk': self.pk})

# 

# New Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order comments with the newest one last (so they appear at the bottom)
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title}'"

    def get_absolute_url(self):
        # Redirect to the post detail page after a comment operation
        return reverse('post_detail', kwargs={'pk': self.post.pk})
    
# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager # NEW IMPORT

# ... (Existing Comment model definition) ...

# Update the Post model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # NEW: Tags field using the TaggableManager
    # This automatically sets up the many-to-many relationship
    tags = TaggableManager() 
    
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

# ... (Keep existing Comment model definition) ...