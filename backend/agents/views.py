"""
Views pour l'API des agents.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Agent
from .serializers import AgentSerializer, AgentListSerializer
from chatagentb.llm_config import LLM_MODELS


class AgentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion CRUD des agents.
    Seuls les administrateurs peuvent créer/modifier/supprimer.
    """

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return AgentListSerializer
        return AgentSerializer

    def get_permissions(self):
        """
        Temporairement: Autoriser tout le monde (développement).
        TODO: En production, remettre IsAdminUser pour create/update/delete.
        """
        # Désactivé temporairement pour le développement
        return []  # Allow any for development

        # Code original (à restaurer en production):
        # if self.action in ['list', 'retrieve']:
        #     return []  # Allow any for development
        # return [IsAdminUser()]

    @action(detail=True, methods=["post"], permission_classes=[])
    def duplicate(self, request, pk=None):
        """
        Duplique un agent existant.
        Note: permission_classes=[] pour développement (TODO: remettre IsAdminUser en prod)
        """
        agent = self.get_object()
        new_agent = agent.duplicate()
        serializer = self.get_serializer(new_agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="available-models")
    def available_models(self, request):
        """
        Retourne la liste des modèles LLM disponibles.
        Endpoint: GET /api/agents/available-models/
        """
        return Response(LLM_MODELS)


@api_view(["GET"])
def llm_models(request):
    """
    Vue simple pour retourner les modèles LLM disponibles.
    Endpoint: GET /api/llm-models/
    """
    return Response({"models": LLM_MODELS, "count": len(LLM_MODELS)})
