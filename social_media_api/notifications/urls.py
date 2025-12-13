# notifications/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notifications')

urlpatterns = [
    # Routes for /notifications/ (list, mark-read, mark-as-read/{pk}/)
    path('', include(router.urls)), 
]