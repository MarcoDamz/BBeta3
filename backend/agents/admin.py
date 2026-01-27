from django.contrib import admin
from .models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'llm_model', 'is_active', 'created_at']
    list_filter = ['llm_model', 'is_active', 'categories']
    search_fields = ['name', 'description', 'system_prompt']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations Générales', {
            'fields': ('name', 'description', 'categories', 'is_active')
        }),
        ('Configuration LLM', {
            'fields': ('llm_model', 'system_prompt', 'temperature', 'max_tokens')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
