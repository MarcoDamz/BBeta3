"""
Modèles pour la gestion des conversations et messages.
"""
from django.db import models
from django.contrib.auth import get_user_model
from agents.models import Agent

User = get_user_model()


class Conversation(models.Model):
    """
    Représente une conversation entre un utilisateur et un ou plusieurs agents.
    """
    CONVERSATION_TYPES = [
        ('user', 'Utilisateur-Agent'),
        ('auto', 'Agent-Agent (Auto-Chat)'),
    ]
    
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Titre",
        help_text="Titre de la conversation (généré automatiquement)"
    )
    
    conversation_type = models.CharField(
        max_length=10,
        choices=CONVERSATION_TYPES,
        default='user',
        verbose_name="Type de conversation"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name="Utilisateur"
    )
    
    agents = models.ManyToManyField(
        Agent,
        related_name='conversations',
        verbose_name="Agents impliqués"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
    
    def __str__(self):
        return self.title or f"Conversation #{self.id}"


class Message(models.Model):
    """
    Représente un message dans une conversation.
    """
    ROLE_CHOICES = [
        ('human', 'Humain'),
        ('ai', 'IA'),
        ('system', 'Système'),
    ]
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Conversation"
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name="Rôle"
    )
    
    content = models.TextField(
        verbose_name="Contenu"
    )
    
    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name="Agent (si AI)"
    )
    
    is_auto_chat = models.BooleanField(
        default=False,
        verbose_name="Auto-Chat",
        help_text="Message généré par le mode Auto-Chat"
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Métadonnées",
        help_text="Informations supplémentaires (tokens, durée, etc.)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"{self.get_role_display()}: {self.content[:50]}..."
