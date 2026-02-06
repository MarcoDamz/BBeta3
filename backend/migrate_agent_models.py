"""
Script pour migrer les agents existants vers les nouveaux noms de modèles.
Utilisez ce script si vous avez changé les clés de modèles dans llm_config.py.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatagentb.settings")
django.setup()

from agents.models import Agent
from chatagentb.llm_config import LLM_MODELS, validate_model_key

# Mapping des anciens noms vers les nouveaux
MODEL_MIGRATION_MAP = {
    # Anciens noms -> Nouveaux noms
    # "azure.gpt-4.1": "gpt-4o",
    # "azure.gpt-4.1-mini": "gpt-4o-mini",
    # "azure.gpt-4o": "gpt-4o",
    # "azure.gpt-4o-mini": "gpt-4o-mini",
    # "azure.gpt-5.1-turbo": "gpt-4-turbo",
    # "gpt-4.1": "gpt-4o",
    # "gpt-4.1-mini": "gpt-4o-mini",
    # "gpt-5.1-turbo": "gpt-4-turbo",
    "gpt-4o": "azure.gpt-4o",
    "gpt-4o-mini": "azure.gpt-4o-mini",
}


def migrate_agents():
    """Migre tous les agents vers les nouveaux noms de modèles."""
    print("🔄 Début de la migration des agents...")
    print(f"📋 Modèles disponibles: {list(LLM_MODELS.keys())}\n")

    agents = Agent.objects.all()
    migrated_count = 0
    already_valid_count = 0
    error_count = 0

    for agent in agents:
        current_model = agent.llm_model

        # Vérifier si le modèle est déjà valide
        if validate_model_key(current_model):
            print(f"✅ Agent '{agent.name}': Modèle '{current_model}' déjà valide")
            already_valid_count += 1
            continue

        # Vérifier si une migration est disponible
        if current_model in MODEL_MIGRATION_MAP:
            new_model = MODEL_MIGRATION_MAP[current_model]
            agent.llm_model = new_model
            agent.save()
            print(
                f"🔄 Agent '{agent.name}': Migré de '{current_model}' vers '{new_model}'"
            )
            migrated_count += 1
        else:
            print(
                f"⚠️  Agent '{agent.name}': Modèle inconnu '{current_model}' - Aucune migration disponible"
            )
            error_count += 1

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA MIGRATION")
    print("=" * 60)
    print(f"Total d'agents: {agents.count()}")
    print(f"✅ Agents déjà valides: {already_valid_count}")
    print(f"🔄 Agents migrés: {migrated_count}")
    print(f"⚠️  Erreurs (modèles inconnus): {error_count}")

    if error_count > 0:
        print("\n⚠️  Certains agents ont des modèles inconnus.")
        print("Vous devez les mettre à jour manuellement dans l'admin Django.")

    print("\n✨ Migration terminée !")


def list_agents_by_model():
    """Liste tous les agents regroupés par modèle."""
    print("\n📊 AGENTS PAR MODÈLE")
    print("=" * 60)

    from django.db.models import Count

    models = Agent.objects.values("llm_model").annotate(count=Count("id"))

    for model_info in models:
        model = model_info["llm_model"]
        count = model_info["count"]
        is_valid = "✅" if validate_model_key(model) else "❌"
        print(f"{is_valid} {model}: {count} agent(s)")


if __name__ == "__main__":
    print("🚀 MIGRATION DES MODÈLES LLM")
    print("=" * 60)

    # Lister d'abord les agents par modèle
    list_agents_by_model()

    # Demander confirmation
    print("\n" + "=" * 60)
    response = input("\n⚠️  Voulez-vous migrer les agents ? (oui/non): ")

    if response.lower() in ["oui", "yes", "o", "y"]:
        migrate_agents()
        print("\n")
        list_agents_by_model()
    else:
        print("\n❌ Migration annulée.")
