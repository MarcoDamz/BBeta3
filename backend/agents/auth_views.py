"""
Views pour l'authentification.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authentifie un utilisateur et retourne ses informations.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Nom d'utilisateur et mot de passe requis."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        # Vérifier si l'utilisateur a accès à l'admin
        is_admin = (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(name="Administrators").exists()
        )

        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "is_admin": is_admin,
                    "groups": list(user.groups.values_list("name", flat=True)),
                }
            }
        )
    else:
        return Response(
            {"detail": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
def logout_view(request):
    """
    Déconnecte l'utilisateur.
    """
    logout(request)
    return Response({"detail": "Déconnexion réussie."})


@api_view(["GET"])
def me_view(request):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    if request.user.is_authenticated:
        # Vérifier si l'utilisateur a accès à l'admin
        is_admin = (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.groups.filter(name="Administrators").exists()
        )

        return Response(
            {
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                    "is_staff": request.user.is_staff,
                    "is_superuser": request.user.is_superuser,
                    "is_admin": is_admin,
                    "groups": list(request.user.groups.values_list("name", flat=True)),
                }
            }
        )
    else:
        return Response(
            {"detail": "Non authentifié."}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Créer un nouveau compte utilisateur
    """
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        email = request.data.get("email", "")

        # Validation
        if not username or not password:
            return Response(
                {"error": "Le nom d'utilisateur et le mot de passe sont requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8:
            return Response(
                {"error": "Le mot de passe doit contenir au moins 8 caractères"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Ce nom d'utilisateur existe déjà"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email and User.objects.filter(email=email).exists():
            return Response(
                {"error": "Cet email est déjà utilisé"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        # Assigner le groupe "Standard Users" par défaut
        standard_group, _ = Group.objects.get_or_create(name="Standard Users")
        user.groups.add(standard_group)

        return Response(
            {
                "message": "Compte créé avec succès",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "groups": list(user.groups.values_list("name", flat=True)),
                },
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
