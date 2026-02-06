"""
Script pour ajouter les colonnes directement dans la base de données.
Usage: docker-compose exec backend python fix_database.py
"""

import os
import sys

# Trouver le bon module de settings
possible_settings = [
    "config.settings",
    "backend.settings",
    "settings",
    "core.settings",
]

settings_module = None
for module in possible_settings:
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", module)
        import django

        django.setup()
        settings_module = module
        break
    except ModuleNotFoundError:
        continue

if not settings_module:
    print("❌ Impossible de trouver le module de settings Django!")
    print("\n🔍 Recherche du fichier settings.py...")

    # Chercher settings.py
    import pathlib

    backend_path = pathlib.Path("/app")
    settings_files = list(backend_path.rglob("settings.py"))

    if settings_files:
        print(f"\n📁 Fichiers settings.py trouvés:")
        for f in settings_files:
            print(f"   - {f}")
            # Essayer de déterminer le module
            relative = f.relative_to(backend_path)
            parts = list(relative.parts[:-1])  # Enlever 'settings.py'
            if parts:
                module_name = ".".join(parts) + ".settings"
                print(f"     Module probable: {module_name}")

    sys.exit(1)

print(f"✅ Module de settings Django trouvé: {settings_module}\n")

from django.db import connection
from django.apps import apps


def find_agent_table():
    """Trouve le nom de la table Agent dans la base de données."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' 
            AND table_name LIKE '%agent%'
            AND table_name NOT LIKE '%django%';
        """
        )
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables contenant 'agent': {tables}")
        return tables[0] if tables else None


def check_and_add_columns():
    """Vérifie et ajoute les colonnes manquantes."""

    # Trouver le nom de la table
    table_name = find_agent_table()

    if not table_name:
        print("❌ Table Agent non trouvée!")
        print("\n📋 Toutes les tables disponibles:")
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public' 
                AND table_name NOT LIKE 'pg_%'
                AND table_name NOT LIKE 'sql_%';
            """
            )
            all_tables = [row[0] for row in cursor.fetchall()]
            for table in all_tables:
                print(f"   - {table}")
        return False

    print(f"✓ Table trouvée: {table_name}")

    with connection.cursor() as cursor:
        # Vérifier les colonnes existantes
        cursor.execute(
            f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='{table_name}';
        """
        )
        existing_columns = [row[0] for row in cursor.fetchall()]

        print(f"\n📋 Colonnes existantes dans {table_name}:")
        for col in existing_columns:
            print(f"   - {col}")

        # Ajouter agent_type si manquant
        if "agent_type" not in existing_columns:
            print("\n➕ Ajout de la colonne 'agent_type'...")
            cursor.execute(
                f"""
                ALTER TABLE {table_name} 
                ADD COLUMN agent_type VARCHAR(10) DEFAULT 'client' NOT NULL;
            """
            )
            cursor.execute(
                f"""
                ALTER TABLE {table_name}
                ADD CONSTRAINT check_agent_type 
                CHECK (agent_type IN ('client', 'metier'));
            """
            )
            print("✅ Colonne 'agent_type' ajoutée avec contrainte")
        else:
            print("\n✓ Colonne 'agent_type' déjà présente")

        # Ajouter first_prompt si manquant
        if "first_prompt" not in existing_columns:
            print("➕ Ajout de la colonne 'first_prompt'...")
            cursor.execute(
                f"""
                ALTER TABLE {table_name} 
                ADD COLUMN first_prompt TEXT NULL;
            """
            )
            print("✅ Colonne 'first_prompt' ajoutée")
        else:
            print("✓ Colonne 'first_prompt' déjà présente")

        # Vérifier à nouveau
        cursor.execute(
            f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='{table_name}'
            AND column_name IN ('agent_type', 'first_prompt');
        """
        )
        final_columns = [row[0] for row in cursor.fetchall()]

        if len(final_columns) == 2:
            print("\n🎉 Toutes les colonnes sont maintenant présentes!")
            print("\n📋 Colonnes ajoutées:")
            print(f"   - agent_type (VARCHAR(10), default='client')")
            print(f"   - first_prompt (TEXT, nullable)")
            print("\n🔄 Prochaines étapes:")
            print("   1. Redémarrer le backend:")
            print("      docker-compose restart backend")
            print("   2. Vérifier l'admin Django:")
            print("      http://localhost:8000/admin/")
            return True
        else:
            print(
                f"\n⚠️  Colonnes manquantes: {set(['agent_type', 'first_prompt']) - set(final_columns)}"
            )
            return False


def show_installed_apps():
    """Affiche les applications Django installées."""
    print("\n📦 Applications Django installées:")
    for app_config in apps.get_app_configs():
        print(f"   - {app_config.label} ({app_config.name})")


if __name__ == "__main__":
    print("🔧 Correction de la base de données...\n")

    # Afficher les apps installées
    show_installed_apps()

    print("\n" + "=" * 60 + "\n")

    try:
        success = check_and_add_columns()
        if success:
            print("\n✅ Base de données corrigée avec succès!")
        else:
            print("\n❌ Échec de la correction")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback

        traceback.print_exc()
