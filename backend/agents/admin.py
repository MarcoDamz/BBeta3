from django.contrib import admin
from .models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["name", "agent_type", "llm_model", "is_active", "created_at"]
    list_filter = ["llm_model", "agent_type", "is_active", "categories"]
    search_fields = ["name", "description", "system_prompt", "first_prompt"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Informations Générales",
            {"fields": ("name", "description", "categories", "is_active")},
        ),
        (
            "Configuration LLM",
            {"fields": ("llm_model", "temperature", "max_tokens")},
        ),
        (
            "Agent Settings",
            {
                "fields": ("agent_type", "system_prompt", "first_prompt"),
                "description": "Le premier prompt est obligatoire pour les agents métier",
            },
        ),
        (
            "Métadonnées",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Personnaliser le formulaire selon le type d'agent.
        """
        form = super().get_form(request, obj, **kwargs)

        # Ajouter des classes CSS personnalisées
        if "agent_type" in form.base_fields:
            form.base_fields["agent_type"].widget.attrs.update(
                {"class": "agent-type-selector"}
            )

        if "first_prompt" in form.base_fields:
            form.base_fields["first_prompt"].widget.attrs.update(
                {
                    "rows": 5,
                    "placeholder": "Message initial pour les agents métier uniquement",
                }
            )

        return form

    def save_model(self, request, obj, form, change):
        """
        Validation supplémentaire lors de la sauvegarde.
        """
        # Nettoyer first_prompt si agent_type = 'client'
        if obj.agent_type == "client":
            obj.first_prompt = None

        super().save_model(request, obj, form, change)
