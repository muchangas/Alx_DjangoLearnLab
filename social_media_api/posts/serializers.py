# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment

# --- Comment Serializer (Must be defined first if nested in PostSerializer) ---

class CommentSerializer(serializers.ModelSerializer):
    # Read-only field to display the comment author's username
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_username', 'post', 'content', 'created_at']
        read_only_fields = ['author', 'post'] # author and post are set automatically by the view

# --- Post Serializer ---

class PostSerializer(serializers.ModelSerializer):
    # Nested representation of comments (for detail view)
    comments = CommentSerializer(many=True, read_only=True)
    
    # Read-only field to display the post author's username
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    # Count of comments for list view efficiency
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 
                  'created_at', 'updated_at', 'comment_count', 'comments']
        read_only_fields = ['author'] # Author is set automatically by the view

    def get_comment_count(self, obj):
        # Efficiently get the count of comments
        return obj.comments.count()