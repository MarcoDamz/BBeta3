"""
Views pour l'authentification.
"""
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authentifie un utilisateur et retourne ses informations.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'detail': 'Nom d\'utilisateur et mot de passe requis.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
        })
    else:
        return Response(
            {'detail': 'Identifiants invalides.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
def logout_view(request):
    """
    Déconnecte l'utilisateur.
    """
    logout(request)
    return Response({'detail': 'Déconnexion réussie.'})


@api_view(['GET'])
def me_view(request):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    if request.user.is_authenticated:
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
            }
        })
    else:
        return Response(
            {'detail': 'Non authentifié.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
