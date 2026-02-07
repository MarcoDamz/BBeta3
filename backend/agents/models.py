"""
Modèles pour la gestion des agents IA.
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from chatagentb.llm_config import get_llm_choices


class Agent(models.Model):
    """
    Représente un agent IA avec ses configurations.
    """

    AGENT_TYPE_CHOICES = [
        ("client", "Client"),
        ("metier", "Métier"),
    ]
    name = models.CharField(
        max_length=200, verbose_name="Nom de l'agent", help_text="Nom unique de l'agent"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description de l'agent et de ses capacités",
    )

    categories = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        verbose_name="Catégories",
        help_text="Tags pour catégoriser l'agent",
    )
    agent_type = models.CharField(
        max_length=10,
        choices=AGENT_TYPE_CHOICES,
        default="client",
        verbose_name="Type d'agent",
        help_text="Client = répond aux questions | Métier = initie la conversation",
    )
    first_prompt = models.TextField(
        blank=True,
        null=True,
        verbose_name="Premier prompt",
        help_text="Message initial pour les agents métier (obligatoire si type = métier)",
    )
    llm_model = models.CharField(
        max_length=50,
        choices=get_llm_choices(),
        verbose_name="Modèle LLM",
        help_text="Modèle de langage utilisé par l'agent",
    )

    system_prompt = models.TextField(
        verbose_name="Prompt Système", help_text="Instructions système pour l'agent"
    )

    temperature = models.FloatField(
        default=0.7,
        verbose_name="Température",
        help_text="Contrôle la créativité (0.0 = déterministe, 1.0 = créatif)",
    )

    max_tokens = models.IntegerField(
        default=2000,
        verbose_name="Tokens Max",
        help_text="Nombre maximum de tokens dans la réponse",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="L'agent est-il actif et disponible ?",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return f"{self.name} ({self.llm_model})"

    def duplicate(self):
        """Crée une copie de l'agent."""
        new_agent = Agent.objects.create(
            name=f"{self.name} (Copie)",
            description=self.description,
            categories=self.categories,
            llm_model=self.llm_model,
            system_prompt=self.system_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            is_active=False,
        )
        return new_agent
