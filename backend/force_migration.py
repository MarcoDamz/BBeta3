"""
Script pour forcer la création de la migration avec les nouveaux champs.
Usage: docker-compose exec backend python force_migration.py
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command
from django.db import connection


def check_columns_exist():
    """Vérifie si les colonnes existent déjà dans la base de données."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='chatagentb_agent' 
            AND column_name IN ('agent_type', 'first_prompt');
        """
        )
        existing_columns = [row[0] for row in cursor.fetchall()]
    return existing_columns


print("🔍 Vérification des colonnes existantes...")
existing = check_columns_exist()

if "agent_type" in existing and "first_prompt" in existing:
    print("✅ Les colonnes existent déjà dans la base de données.")
    print("⚠️  Django pense qu'il n'y a rien à migrer car les colonnes existent déjà.")
    print("\n💡 Solutions possibles:")
    print("   1. Utiliser --fake pour marquer la migration comme appliquée")
    print("   2. Ou recréer la base de données depuis zéro")
    sys.exit(0)

print(f"📋 Colonnes existantes: {existing}")
print("\n🔄 Création de la migration...")

try:
    # Créer la migration
    call_command(
        "makemigrations",
        "chatagentb",
        "--name",
        "add_agent_type_and_first_prompt",
        verbosity=2,
    )
    print("\n✅ Migration créée avec succès!")
    print("\n📝 Appliquer la migration avec:")
    print("   docker-compose exec backend python manage.py migrate")

except Exception as e:
    print(f"\n❌ Erreur lors de la création de la migration: {e}")
    sys.exit(1)
