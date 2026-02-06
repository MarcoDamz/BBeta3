"""
URLs pour l'API des agents.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, llm_models

router = DefaultRouter()
router.register(r"", AgentViewSet, basename="agent")

urlpatterns = [
    # ViewSet routes (CRUD agents)
    # GET    /api/agents/                    → list
    # POST   /api/agents/                    → create
    # GET    /api/agents/<id>/               → retrieve
    # PUT    /api/agents/<id>/               → update
    # DELETE /api/agents/<id>/               → destroy
    # GET    /api/agents/available-models/   → available_models
    path("", include(router.urls)),
    # Vue simple pour les modèles LLM
    # GET /api/agents/llm-models/
    path("llm-models/", llm_models, name="llm-models"),
]
