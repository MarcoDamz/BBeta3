"""
Serializers pour l'API de chat.
"""

from rest_framework import serializers
from .models import Conversation, Message, Folder
from agents.serializers import AgentListSerializer


class FolderSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Folder."""

    subfolders = serializers.SerializerMethodField()
    conversations_count = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = [
            "id",
            "name",
            "parent",
            "order",
            "created_at",
            "updated_at",
            "subfolders",
            "conversations_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_subfolders(self, obj):
        if hasattr(obj, "subfolders"):
            subfolders = obj.subfolders.all()
            return FolderSerializer(subfolders, many=True).data
        return []

    def get_conversations_count(self, obj):
        return obj.conversations.count()


class MessageSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Message."""

    agent_name = serializers.CharField(source="agent.name", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "role",
            "content",
            "agent",
            "agent_name",
            "is_auto_chat",
            "metadata",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "agent_name"]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Conversation."""

    messages = MessageSerializer(many=True, read_only=True)
    agents_details = AgentListSerializer(source="agents", many=True, read_only=True)
    message_count = serializers.IntegerField(source="messages.count", read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "conversation_type",
            "user",
            "agents",
            "agents_details",
            "messages",
            "message_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "message_count"]


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des conversations."""

    agents_details = AgentListSerializer(source="agents", many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    message_count = serializers.IntegerField(source="messages.count", read_only=True)
    folder_name = serializers.CharField(
        source="folder.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "conversation_type",
            "folder",
            "folder_name",
            "agents_details",
            "message_count",
            "last_message",
            "created_at",
            "updated_at",
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                "content": last_msg.content[:100],
                "role": last_msg.role,
                "created_at": last_msg.created_at,
            }
        return None


class ChatMessageInputSerializer(serializers.Serializer):
    """Serializer pour les messages envoyés par l'utilisateur."""

    message = serializers.CharField()
    agent_id = serializers.IntegerField()
    conversation_id = serializers.IntegerField(required=False, allow_null=True)


class AutoChatInputSerializer(serializers.Serializer):
    """Serializer pour le mode Auto-Chat."""

    agent_a_id = serializers.IntegerField()
    agent_b_id = serializers.IntegerField()
    initial_message = serializers.CharField()
    iterations = serializers.IntegerField(min_value=1, max_value=50)
