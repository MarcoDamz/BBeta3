"""
Custom authentication classes for the API.
"""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication without CSRF checks for API endpoints.
    Use only for development or with proper CORS configuration.
    """
    def enforce_csrf(self, request):
        return  # Skip CSRF check
