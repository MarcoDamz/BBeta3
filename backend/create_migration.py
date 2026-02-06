"""
Script pour créer manuellement la migration des nouveaux champs.
À exécuter : docker-compose exec backend python create_migration.py
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command

print("🔄 Création de la migration pour les champs agent_type et first_prompt...")
call_command(
    "makemigrations", "chatagentb", "--name", "add_agent_type_and_first_prompt"
)

print("✅ Migration créée avec succès!")
print("\n📝 Prochaine étape : Appliquer la migration avec :")
print("   docker-compose exec backend python manage.py migrate")
