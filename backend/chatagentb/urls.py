"""
URL configuration for chatagentb project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agents.auth_views import login_view, logout_view, me_view, register_view
from django.http import JsonResponse


# WhiteNoise will automatically serve static files in production
# No need for the DEBUG check anymore
def health_check(request):
    """Vue simple pour vérifier que le serveur fonctionne."""
    return JsonResponse({"status": "ok", "message": "ChatAgentB API is running"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
    path("api/agents/", include("agents.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/auth/login/", login_view, name="login"),
    path("api/auth/logout/", logout_view, name="logout"),
    path("api/auth/me/", me_view, name="me"),
    path("api/register/", register_view, name="register"),
]
