"""
Tâches Celery pour les opérations asynchrones.
"""
from celery import shared_task
from django.contrib.auth import get_user_model
from agents.models import Agent
from chat.models import Conversation, Message
from chat.llm_service import LLMService

User = get_user_model()


@shared_task
def generate_conversation_title(conversation_id: int):
    """
    Génère un titre pour une conversation en utilisant le premier message.
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        
        # Si la conversation a déjà un titre, ne rien faire
        if conversation.title:
            return f"Conversation {conversation_id} a déjà un titre"
        
        # Récupérer le premier message humain
        first_message = conversation.messages.filter(role='human').first()
        if not first_message:
            return f"Aucun message humain trouvé pour la conversation {conversation_id}"
        
        # Générer le titre
        title = LLMService.generate_title(first_message.content)
        
        # Sauvegarder
        conversation.title = title
        conversation.save(update_fields=['title'])
        
        return f"Titre généré pour la conversation {conversation_id}: {title}"
    
    except Conversation.DoesNotExist:
        return f"Conversation {conversation_id} introuvable"
    except Exception as e:
        return f"Erreur lors de la génération du titre: {str(e)}"


@shared_task
def run_auto_chat(agent_a_id: int, agent_b_id: int, initial_message: str, 
                  iterations: int, user_id: int):
    """
    Exécute une conversation automatique entre deux agents.
    """
    try:
        agent_a = Agent.objects.get(id=agent_a_id)
        agent_b = Agent.objects.get(id=agent_b_id)
        user = User.objects.get(id=user_id)
        
        # Créer la conversation
        conversation = Conversation.objects.create(
            title=f"AUTO: {agent_a.name} ↔ {agent_b.name}",
            conversation_type='auto',
            user=user
        )
        conversation.agents.add(agent_a, agent_b)
        
        # Message initial
        Message.objects.create(
            conversation=conversation,
            role='human',
            content=initial_message,
            is_auto_chat=True
        )
        
        # Historique de conversation
        history = [{'role': 'human', 'content': initial_message}]
        
        # Alternance entre les deux agents
        for i in range(iterations):
            # Agent A répond
            current_agent = agent_a if i % 2 == 0 else agent_b
            
            response = LLMService.generate_response(current_agent, history)
            
            # Sauvegarder le message
            Message.objects.create(
                conversation=conversation,
                role='ai',
                content=response,
                agent=current_agent,
                is_auto_chat=True,
                metadata={'iteration': i + 1}
            )
            
            # Ajouter à l'historique
            history.append({'role': 'ai', 'content': response})
            
            # Préparer le prochain tour (le message de l'IA devient le prompt pour l'autre agent)
            history.append({'role': 'human', 'content': response})
        
        return {
            'status': 'success',
            'conversation_id': conversation.id,
            'total_messages': iterations + 1,
            'message': f"Auto-chat terminé: {iterations} échanges entre {agent_a.name} et {agent_b.name}"
        }
    
    except Agent.DoesNotExist:
        return {'status': 'error', 'message': 'Un ou plusieurs agents introuvables'}
    except User.DoesNotExist:
        return {'status': 'error', 'message': 'Utilisateur introuvable'}
    except Exception as e:
        return {'status': 'error', 'message': f'Erreur: {str(e)}'}
