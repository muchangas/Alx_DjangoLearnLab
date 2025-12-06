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