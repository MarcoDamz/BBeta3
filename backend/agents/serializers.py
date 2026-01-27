"""
Serializers pour l'API des agents.
"""
from rest_framework import serializers
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Agent."""
    
    class Meta:
        model = Agent
        fields = [
            'id',
            'name',
            'description',
            'categories',
            'llm_model',
            'system_prompt',
            'temperature',
            'max_tokens',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AgentListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des agents."""
    
    class Meta:
        model = Agent
        fields = [
            'id',
            'name',
            'description',
            'categories',
            'llm_model',
            'is_active'
        ]
