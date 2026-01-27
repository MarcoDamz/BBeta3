"""
Views pour l'API de chat.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Prefetch
from agents.models import Agent
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer,
    ChatMessageInputSerializer,
    AutoChatInputSerializer
)
from .llm_service import LLMService
from .tasks import generate_conversation_title, run_auto_chat


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtre les conversations de l'utilisateur connecté."""
        return Conversation.objects.filter(
            user=self.request.user
        ).prefetch_related(
            'agents',
            Prefetch('messages', queryset=Message.objects.select_related('agent'))
        )
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def perform_create(self, serializer):
        """Associe la conversation à l'utilisateur connecté."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Envoie un message et obtient une réponse de l'agent.
        """
        serializer = ChatMessageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message_content = serializer.validated_data['message']
        agent_id = serializer.validated_data['agent_id']
        conversation_id = serializer.validated_data.get('conversation_id')
        
        try:
            agent = Agent.objects.get(id=agent_id, is_active=True)
        except Agent.DoesNotExist:
            return Response(
                {'error': 'Agent introuvable ou inactif'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Créer ou récupérer la conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id,
                    user=request.user
                )
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation introuvable'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            conversation = Conversation.objects.create(user=request.user)
            conversation.agents.add(agent)
        
        # Sauvegarder le message de l'utilisateur
        user_message = Message.objects.create(
            conversation=conversation,
            role='human',
            content=message_content
        )
        
        # Générer le titre si c'est le premier message
        if conversation.messages.count() == 1:
            generate_conversation_title.delay(conversation.id)
        
        # Construire l'historique de conversation
        history = [
            {
                'role': msg.role,
                'content': msg.content
            }
            for msg in conversation.messages.all()
        ]
        
        # Générer la réponse de l'agent
        try:
            response_content = LLMService.generate_response(agent, history)
            
            # Sauvegarder la réponse
            ai_message = Message.objects.create(
                conversation=conversation,
                role='ai',
                content=response_content,
                agent=agent
            )
            
            return Response({
                'conversation_id': conversation.id,
                'user_message': MessageSerializer(user_message).data,
                'ai_message': MessageSerializer(ai_message).data
            })
        
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la génération de la réponse: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def auto_chat(self, request):
        """
        Lance une conversation automatique entre deux agents.
        Réservé aux administrateurs.
        """
        serializer = AutoChatInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        agent_a_id = serializer.validated_data['agent_a_id']
        agent_b_id = serializer.validated_data['agent_b_id']
        initial_message = serializer.validated_data['initial_message']
        iterations = serializer.validated_data['iterations']
        
        # Vérifier que les agents existent
        try:
            Agent.objects.get(id=agent_a_id, is_active=True)
            Agent.objects.get(id=agent_b_id, is_active=True)
        except Agent.DoesNotExist:
            return Response(
                {'error': 'Un ou plusieurs agents introuvables ou inactifs'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Lancer la tâche asynchrone
        task = run_auto_chat.delay(
            agent_a_id=agent_a_id,
            agent_b_id=agent_b_id,
            initial_message=initial_message,
            iterations=iterations,
            user_id=request.user.id
        )
        
        return Response({
            'status': 'started',
            'task_id': task.id,
            'message': f'Auto-chat lancé avec {iterations} itérations'
        }, status=status.HTTP_202_ACCEPTED)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour la lecture des messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtre les messages des conversations de l'utilisateur."""
        return Message.objects.filter(
            conversation__user=self.request.user
        ).select_related('conversation', 'agent')
