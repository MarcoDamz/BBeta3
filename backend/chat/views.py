"""
Views pour l'API de chat.
"""

import logging
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
    AutoChatInputSerializer,
)
from .llm_service import LLMService
from .tasks import generate_conversation_title, run_auto_chat

logger = logging.getLogger(__name__)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des conversations.
    """

    serializer_class = ConversationSerializer
    # Temporairement AllowAny pour le développement
    # TODO: Remettre IsAuthenticated après avoir configuré les sessions correctement
    permission_classes = []

    def get_queryset(self):
        """Filtre les conversations de l'utilisateur connecté (si authentifié)."""
        if self.request.user.is_authenticated:
            return Conversation.objects.filter(user=self.request.user).prefetch_related(
                "agents",
                Prefetch("messages", queryset=Message.objects.select_related("agent")),
            )
        # Si non authentifié, retourner toutes les conversations (dev only)
        return Conversation.objects.all().prefetch_related(
            "agents",
            Prefetch("messages", queryset=Message.objects.select_related("agent")),
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ConversationListSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        """Associe la conversation à l'utilisateur connecté (si authentifié)."""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Pour le dev: créer sans user (nécessite de rendre user nullable)
            # Ou utiliser un user par défaut
            from django.contrib.auth import get_user_model

            User = get_user_model()
            default_user = User.objects.filter(is_superuser=True).first()
            serializer.save(user=default_user)

    @action(detail=False, methods=["post"])
    def send_message(self, request):
        """
        Envoie un message et obtient une réponse de l'agent.
        """
        try:
            logger.info(f"Received send_message request: {request.data}")

            serializer = ChatMessageInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            message_content = serializer.validated_data["message"]
            agent_id = serializer.validated_data["agent_id"]
            conversation_id = serializer.validated_data.get("conversation_id")

            logger.info(
                f"Message: {message_content}, Agent: {agent_id}, Conversation: {conversation_id}"
            )

            try:
                agent = Agent.objects.get(id=agent_id, is_active=True)
                logger.info(f"Agent found: {agent.name}")
            except Agent.DoesNotExist:
                logger.error(f"Agent not found: {agent_id}")
                return Response(
                    {"error": "Agent introuvable ou inactif"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Obtenir l'utilisateur (authentifié ou par défaut)
            if request.user.is_authenticated:
                user = request.user
                logger.info(f"Authenticated user: {user.username}")
            else:
                from django.contrib.auth import get_user_model

                User = get_user_model()
                user = User.objects.filter(is_superuser=True).first()
                if not user:
                    logger.error("No default superuser found")
                    return Response(
                        {"error": "Aucun utilisateur par défaut trouvé"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                logger.info(f"Using default user: {user.username}")

            # Créer ou récupérer la conversation
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(
                        id=conversation_id, user=user
                    )
                    logger.info(f"Existing conversation found: {conversation.id}")
                except Conversation.DoesNotExist:
                    logger.error(f"Conversation not found: {conversation_id}")
                    return Response(
                        {"error": "Conversation introuvable"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                conversation = Conversation.objects.create(user=user)
                conversation.agents.add(agent)
                logger.info(f"New conversation created: {conversation.id}")

            # Sauvegarder le message de l'utilisateur
            user_message = Message.objects.create(
                conversation=conversation, role="human", content=message_content
            )
            logger.info(f"User message saved: {user_message.id}")

            # Générer le titre si c'est le premier message
            if conversation.messages.count() == 1:
                logger.info("Triggering title generation")
                generate_conversation_title.delay(conversation.id)

            # Construire l'historique de conversation
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation.messages.all()
            ]
            logger.info(f"History constructed with {len(history)} messages")

            # Générer la réponse de l'agent
            try:
                logger.info("Calling LLMService.generate_response")
                response_content = LLMService.generate_response(agent, history)
                logger.info(f"LLM response received: {response_content[:100]}...")

                # Sauvegarder la réponse
                ai_message = Message.objects.create(
                    conversation=conversation,
                    role="ai",
                    content=response_content,
                    agent=agent,
                )
                logger.info(f"AI message saved: {ai_message.id}")

                return Response(
                    {
                        "conversation_id": conversation.id,
                        "user_message": MessageSerializer(user_message).data,
                        "ai_message": MessageSerializer(ai_message).data,
                    }
                )

            except Exception as e:
                logger.error(f"Error generating LLM response: {str(e)}", exc_info=True)
                return Response(
                    {"error": f"Erreur lors de la génération de la réponse: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            logger.error(f"Unexpected error in send_message: {str(e)}", exc_info=True)
            return Response(
                {"error": f"Erreur inattendue: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def auto_chat(self, request):
        """
        Lance une conversation automatique entre deux agents.
        Réservé aux administrateurs.
        """
        serializer = AutoChatInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agent_a_id = serializer.validated_data["agent_a_id"]
        agent_b_id = serializer.validated_data["agent_b_id"]
        initial_message = serializer.validated_data["initial_message"]
        iterations = serializer.validated_data["iterations"]

        # Vérifier que les agents existent
        try:
            Agent.objects.get(id=agent_a_id, is_active=True)
            Agent.objects.get(id=agent_b_id, is_active=True)
        except Agent.DoesNotExist:
            return Response(
                {"error": "Un ou plusieurs agents introuvables ou inactifs"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Lancer la tâche asynchrone
        task = run_auto_chat.delay(
            agent_a_id=agent_a_id,
            agent_b_id=agent_b_id,
            initial_message=initial_message,
            iterations=iterations,
            user_id=request.user.id,
        )

        return Response(
            {
                "status": "started",
                "task_id": task.id,
                "message": f"Auto-chat lancé avec {iterations} itérations",
            },
            status=status.HTTP_202_ACCEPTED,
        )


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
        ).select_related("conversation", "agent")
