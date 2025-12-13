# posts/models.py

from django.db import models
from django.conf import settings # Best practice to refer to the active user model

class Post(models.Model):
    # ForeignKey to the CustomUser model defined by AUTH_USER_MODEL
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Auto-managed date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Default order: newest first

    def __str__(self):
        return f'{self.title} by {self.author.username}'

class Comment(models.Model):
    # ForeignKey to the Post model it belongs to
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # ForeignKey to the CustomUser who authored the comment
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    
    # Auto-managed date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Default order: oldest first

    def __str__(self):
        return f'Comment by {self.author.username} on post "{self.post.title[:20]}..."'
# posts/models.py (Add to existing content)

from django.db import models
from django.conf import settings
# ... (Existing Post and Comment models) ...

class Like(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='liked_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only like a post once
        unique_together = ('post', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'