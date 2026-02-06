"""
Serializers pour l'application agents.
"""

from rest_framework import serializers
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Agent.
    """

    # Champ calculé pour afficher le nom du modèle LLM
    # llm_model_display = serializers.CharField(
    #     source="get_llm_model_display", read_only=True
    # )

    # # Champ calculé pour afficher le type d'agent
    # agent_type_display = serializers.CharField(
    #     source="get_agent_type_display", read_only=True
    # )

    class Meta:
        model = Agent
        fields = [
            "id",
            "name",
            "description",
            "categories",
            "agent_type",
            "first_prompt",
            "system_prompt",
            "llm_model",
            "temperature",
            "max_tokens",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """
        Validation personnalisée.
        """
        agent_type = data.get("agent_type")
        first_prompt = data.get("first_prompt")

        # Vérifier que first_prompt est présent pour les agents métier
        if agent_type == "metier" and not first_prompt:
            raise serializers.ValidationError(
                {
                    "first_prompt": "Le premier prompt est obligatoire pour un agent de type métier."
                }
            )

        # Nettoyer first_prompt pour les agents client
        if agent_type == "client" and first_prompt:
            data["first_prompt"] = None

        return data


class AgentListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des agents."""

    class Meta:
        model = Agent
        fields = [
            "id",
            "name",
            "description",
            "categories",
            "agent_type",
            "first_prompt",
            "system_prompt",
            "llm_model",
            "temperature",
            "max_tokens",
            "is_active",
        ]
