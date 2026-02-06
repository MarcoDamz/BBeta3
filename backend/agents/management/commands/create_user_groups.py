"""
Commande pour créer les groupes d'utilisateurs.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from agents.models import Agent


class Command(BaseCommand):
    help = "Crée les groupes d'utilisateurs par défaut"

    def handle(self, *args, **options):
        # Créer le groupe "Standard Users"
        standard_group, created = Group.objects.get_or_create(name="Standard Users")

        if created:
            self.stdout.write(
                self.style.SUCCESS('Groupe "Standard Users" créé avec succès')
            )

            # Permissions pour les utilisateurs standards (pas d'accès admin)
            content_type = ContentType.objects.get_for_model(Agent)

            # Uniquement les permissions de lecture
            view_permission = Permission.objects.get(
                codename="view_agent",
                content_type=content_type,
            )
            standard_group.permissions.add(view_permission)

            self.stdout.write(
                self.style.SUCCESS('Permissions configurées pour "Standard Users"')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Le groupe "Standard Users" existe déjà')
            )

        # Créer le groupe "Administrators"
        admin_group, created = Group.objects.get_or_create(name="Administrators")

        if created:
            self.stdout.write(
                self.style.SUCCESS('Groupe "Administrators" créé avec succès')
            )

            # Permissions complètes pour les administrateurs
            content_type = ContentType.objects.get_for_model(Agent)
            permissions = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.set(permissions)

            self.stdout.write(
                self.style.SUCCESS('Permissions configurées pour "Administrators"')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Le groupe "Administrators" existe déjà')
            )

        self.stdout.write(self.style.SUCCESS("Configuration des groupes terminée !"))
