"""
Configuration centralisée des modèles LLM.
"""

# Configuration des modèles LLM disponibles
LLM_MODELS = {
    # OpenAI Models
    "gpt-4o": {
        "display_name": "GPT-4o",
        "provider": "openai",
        "model_name": "gpt-4o",
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
    "gpt-4o-mini": {
        "display_name": "GPT-4o Mini",
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
    "gpt-4-turbo": {
        "display_name": "GPT-4 Turbo",
        "provider": "openai",
        "model_name": "gpt-4-turbo",
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
    "gpt-4": {
        "display_name": "GPT-4",
        "provider": "openai",
        "model_name": "gpt-4",
        "max_tokens_limit": 8192,
        "supports_streaming": True,
    },
    "gpt-3.5-turbo": {
        "display_name": "GPT-3.5 Turbo",
        "provider": "openai",
        "model_name": "gpt-3.5-turbo",
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
    # Azure OpenAI Models (si vous utilisez Azure)
    "azure.gpt-4o": {
        "display_name": "litellm Azure GPT-4o",
        "provider": "azure",
        "model_name": "azure.gpt-4o",
        # "deployment_name": "gpt-4o",  # Nom du déploiement Azure
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
    "azure.gpt-4o-mini": {
        "display_name": "litellm Azure GPT-4o Mini",
        "provider": "azure",
        "model_name": "azure.gpt-4o-mini",
        # "deployment_name": "gpt-4o-mini",
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
}

# Modèle par défaut pour la génération de titres
DEFAULT_TITLE_MODEL = "gpt-3.5-turbo"

# Modèle par défaut pour les nouveaux agents
DEFAULT_AGENT_MODEL = "gpt-4o-mini"


def get_llm_choices():
    """
    Retourne la liste des choix de modèles LLM pour Django.
    Format: [(key, display_name), ...]
    """
    return [(key, config["display_name"]) for key, config in LLM_MODELS.items()]


def get_model_config(model_key: str) -> dict:
    """
    Retourne la configuration d'un modèle LLM.

    Args:
        model_key: Clé du modèle (ex: 'gpt-4o', 'claude-3-opus')

    Returns:
        dict: Configuration du modèle

    Raises:
        KeyError: Si le modèle n'existe pas
    """
    if model_key not in LLM_MODELS:
        raise KeyError(f"Modèle LLM '{model_key}' non trouvé dans la configuration")
    return LLM_MODELS[model_key]


def get_provider_models(provider: str) -> dict:
    """
    Retourne tous les modèles d'un provider spécifique.

    Args:
        provider: Nom du provider ('openai', 'azure', 'anthropic')

    Returns:
        dict: Dictionnaire des modèles du provider
    """
    return {
        key: config
        for key, config in LLM_MODELS.items()
        if config["provider"] == provider
    }


def validate_model_key(model_key: str) -> bool:
    """
    Vérifie si une clé de modèle existe.

    Args:
        model_key: Clé du modèle à vérifier

    Returns:
        bool: True si le modèle existe, False sinon
    """
    return model_key in LLM_MODELS
