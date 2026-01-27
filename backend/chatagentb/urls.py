"""
URL configuration for chatagentb project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agents.auth_views import login_view, logout_view, me_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/agents/', include('agents.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/me/', me_view, name='me'),
]

# Serve static files in development/Docker
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
