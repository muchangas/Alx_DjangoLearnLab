# notifications/serializers.py

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Display the actor's username
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    
    # Display the target object type (e.g., 'Post', 'CustomUser')
    target_type = serializers.CharField(source='content_type.model', read_only=True)
    
    # Optional: Display a summary of the target object
    # For simplicity, we just show the actor and verb
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 
                  'target_type', 'object_id', 'timestamp', 'is_read']
        read_only_fields = ['recipient', 'actor', 'verb', 'timestamp']