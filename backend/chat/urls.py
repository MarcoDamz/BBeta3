"""
URLs pour l'API de chat.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, FolderViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"folders", FolderViewSet, basename="folder")

urlpatterns = [
    path("", include(router.urls)),
]
