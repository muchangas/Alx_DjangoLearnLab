# notifications/tasks.py

from django.contrib.contenttypes.models import ContentType
from .models import Notification
from accounts.models import CustomUser # Import CustomUser for follow notification

def create_notification_async(recipient, actor, verb, target):
    """
    Creates a Notification instance based on the provided action.
    This mimics an asynchronous task or signal handler.
    """
    if recipient == actor:
        # Don't notify users about their own actions
        return

    # Get the ContentType object for the target
    target_content_type = ContentType.objects.get_for_model(target)
    
    # Create the notification
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target,
        content_type=target_content_type,
        object_id=target.pk,
    )

def notify_user_followed(follower, followed):
    """
    Specific task for a new follower notification.
    """
    create_notification_async(
        recipient=followed,
        actor=follower,
        verb='followed',
        target=follower # The target is the user who followed (actor)
    )