# notifications/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer

class NotificationPagination(PageNumberPagination):
    page_size = 20

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allows users to view their notifications and mark them as read.
    ReadOnlyModelViewSet ensures no creation/deletion via this endpoint.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        # Only show notifications meant for the authenticated user
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=False, methods=['patch'], url_path='mark-read')
    def mark_all_as_read(self, request):
        """
        Marks all unread notifications for the current user as read.
        """
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """
        Marks a specific notification as read.
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)