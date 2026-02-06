# Configuration des Modèles LLM

Ce document explique comment gérer la configuration centralisée des modèles LLM dans ChatAgentB.

## 📁 Fichier de Configuration Centralisé

Tous les modèles LLM sont définis dans un seul fichier :
```
backend/chatagentb/llm_config.py
```

## 🎯 Avantages de la Configuration Centralisée

1. **Un seul endroit à modifier** : Tous les modèles sont définis dans `llm_config.py`
2. **Cohérence** : Les mêmes modèles sont disponibles partout dans l'application
3. **Facilité d'ajout** : Ajouter un nouveau modèle nécessite une seule modification
4. **Validation** : Des fonctions de validation intégrées
5. **Multi-provider** : Support pour OpenAI, Azure OpenAI, et Anthropic

## 🔧 Ajouter un Nouveau Modèle LLM

### 1. Éditer `backend/chatagentb/llm_config.py`

Ajoutez votre modèle au dictionnaire `LLM_MODELS` :

```python
LLM_MODELS = {
    # ... autres modèles ...
    
    "mon-nouveau-modele": {
        "display_name": "Mon Nouveau Modèle",
        "provider": "openai",  # ou "azure" ou "anthropic"
        "model_name": "gpt-4-turbo-2024-04-09",
        "max_tokens_limit": 4096,
        "supports_streaming": True,
    },
}
```

### 2. Configuration Azure (si nécessaire)

Pour un modèle Azure OpenAI, ajoutez le `deployment_name` :

```python
"azure.gpt-4": {
    "display_name": "Azure GPT-4",
    "provider": "azure",
    "model_name": "gpt-4",
    "deployment_name": "mon-deploiement-gpt4",  # Nom dans Azure
    "max_tokens_limit": 8192,
    "supports_streaming": True,
},
```

### 3. Configuration Anthropic (si nécessaire)

Pour un modèle Claude :

```python
"claude-3.5-sonnet": {
    "display_name": "Claude 3.5 Sonnet",
    "provider": "anthropic",
    "model_name": "claude-3-5-sonnet-20241022",
    "max_tokens_limit": 4096,
    "supports_streaming": True,
},
```

## 🔐 Configuration des Clés API

### Fichier `.env`

Configurez vos clés API dans le fichier `.env` :

```bash
# ============ OpenAI API ============
OPENAI_API_KEY=sk-votre-cle-openai-ici

# ============ Azure OpenAI (Optionnel) ============
AZURE_OPENAI_API_KEY=votre-cle-azure-ici
AZURE_OPENAI_ENDPOINT=https://votre-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# ============ Anthropic (Optionnel) ============
ANTHROPIC_API_KEY=votre-cle-anthropic-ici
```

## 📝 Modifier le Modèle par Défaut

Dans `backend/chatagentb/llm_config.py` :

```python
# Modèle par défaut pour la génération de titres
DEFAULT_TITLE_MODEL = "gpt-3.5-turbo"  # ← Modifier ici

# Modèle par défaut pour les nouveaux agents
DEFAULT_AGENT_MODEL = "gpt-4o-mini"  # ← Modifier ici
```

## 🔍 Utilisation dans le Code

### Récupérer la Configuration d'un Modèle

```python
from chatagentb.llm_config import get_model_config

model_config = get_model_config("gpt-4o")
print(model_config)
# {
#     "display_name": "GPT-4o",
#     "provider": "openai",
#     "model_name": "gpt-4o",
#     "max_tokens_limit": 4096,
#     "supports_streaming": True,
# }
```

### Lister Tous les Modèles d'un Provider

```python
from chatagentb.llm_config import get_provider_models

openai_models = get_provider_models("openai")
azure_models = get_provider_models("azure")
anthropic_models = get_provider_models("anthropic")
```

### Valider un Modèle

```python
from chatagentb.llm_config import validate_model_key

if validate_model_key("gpt-4o"):
    print("Modèle valide !")
```

## 🚀 Modèles Actuellement Disponibles

### OpenAI
- `gpt-4o` - GPT-4o
- `gpt-4o-mini` - GPT-4o Mini
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-4` - GPT-4
- `gpt-3.5-turbo` - GPT-3.5 Turbo

### Azure OpenAI
- `azure.gpt-4o` - Azure GPT-4o
- `azure.gpt-4o-mini` - Azure GPT-4o Mini

### Anthropic
- `claude-3-opus` - Claude 3 Opus
- `claude-3-sonnet` - Claude 3 Sonnet
- `claude-3-haiku` - Claude 3 Haiku

## 🔄 Mise à Jour après Modification

Après avoir modifié `llm_config.py`, les changements sont automatiques :

1. **En développement** : Le serveur se recharge automatiquement (hot reload)
2. **En production** : Redémarrez le conteneur backend :
   ```bash
   docker-compose restart backend
   ```

## 🧪 Migration des Agents Existants

Si vous changez la clé d'un modèle, vous devrez peut-être mettre à jour les agents existants dans la base de données.

### Script de migration (Django shell) :

```python
python manage.py shell

# Dans le shell Django
from agents.models import Agent

# Mettre à jour tous les agents utilisant l'ancien modèle
Agent.objects.filter(llm_model="ancien-modele").update(llm_model="nouveau-modele")
```

## 📊 Structure du Modèle

Chaque modèle doit avoir cette structure :

```python
"cle-unique": {
    "display_name": str,        # Nom affiché dans l'interface
    "provider": str,            # "openai", "azure", ou "anthropic"
    "model_name": str,          # Nom du modèle chez le provider
    "deployment_name": str,     # (Azure seulement) Nom du déploiement
    "max_tokens_limit": int,    # Limite de tokens
    "supports_streaming": bool, # Support du streaming
}
```

## ⚠️ Notes Importantes

1. **Clés uniques** : Chaque clé de modèle doit être unique dans `LLM_MODELS`
2. **Noms de provider** : Uniquement `"openai"`, `"azure"`, ou `"anthropic"`
3. **API Keys** : Assurez-vous que les clés API sont configurées dans `.env`
4. **Migrations** : Après modification, créez une migration Django si nécessaire

## 🆘 Dépannage

### Erreur : "Modèle LLM 'xxx' non trouvé"
- Vérifiez que le modèle existe dans `LLM_MODELS`
- Vérifiez l'orthographe de la clé

### Erreur : "Provider 'xxx' non supporté"
- Le provider doit être `"openai"`, `"azure"`, ou `"anthropic"`

### Erreur : "API Key manquante"
- Vérifiez que la clé API est dans le fichier `.env`
- Redémarrez les conteneurs Docker

## 📚 Ressources

- [Documentation OpenAI](https://platform.openai.com/docs/models)
- [Documentation Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai/)
- [Documentation Anthropic](https://docs.anthropic.com/claude/docs)
- [Documentation LangChain](https://python.langchain.com/docs/get_started/introduction)
