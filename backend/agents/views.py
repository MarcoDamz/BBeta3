"""
Views pour l'API des agents.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Agent
from .serializers import AgentSerializer, AgentListSerializer


class AgentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion CRUD des agents.
    Seuls les administrateurs peuvent créer/modifier/supprimer.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AgentListSerializer
        return AgentSerializer
    
    def get_permissions(self):
        """
        Allow anyone to read (for development).
        Only admins can create/modify/delete.
        """
        if self.action in ['list', 'retrieve']:
            return []  # Allow any for development
        return [IsAdminUser()]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def duplicate(self, request, pk=None):
        """
        Duplique un agent existant.
        """
        agent = self.get_object()
        new_agent = agent.duplicate()
        serializer = self.get_serializer(new_agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
