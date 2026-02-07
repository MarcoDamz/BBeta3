# 📚 Documentation des Fonctionnalités - ChatAgentB

Ce dossier contient la documentation détaillée de toutes les fonctionnalités de ChatAgentB.

## 📑 Index des fonctionnalités

### 🗂️ Système de dossiers (v1.1.0)
Organisation des conversations en dossiers avec support du drag & drop.

- **[📖 Documentation technique complète](FOLDERS_FEATURE.md)** - Architecture, API, schéma DB
- **[🚀 Guide de démarrage rapide](FOLDERS_QUICKSTART.md)** - Comment utiliser la fonctionnalité
- **[✅ Récapitulatif d'implémentation](FOLDERS_IMPLEMENTATION_COMPLETE.md)** - État de l'implémentation

**Fonctionnalités** :
- ✅ Création de dossiers
- ✅ Arborescence (dossiers/sous-dossiers)
- ✅ Drag & Drop des conversations
- ✅ Renommage et suppression
- ✅ Compteurs de conversations
- ✅ Zone "Non classées"
- ✅ Persistence en base de données

**Endpoints API** :
```
GET    /api/chat/folders/
POST   /api/chat/folders/
GET    /api/chat/folders/{id}/
PATCH  /api/chat/folders/{id}/
DELETE /api/chat/folders/{id}/
POST   /api/chat/folders/reorder/
POST   /api/chat/conversations/{id}/move_to_folder/
```

---

## 🎯 Fonctionnalités principales (v1.0.0)

### 💬 Système de chat
- Conversations avec agents IA multiples
- Support OpenAI et Anthropic
- Messages persistants
- Génération automatique de titres

### 🤖 Gestion des agents
- CRUD complet via API
- Configuration de modèles LLM
- Paramètres de température et tokens
- Instructions système personnalisables

### 🔄 Mode Auto-Chat
- Conversation automatique entre 2 agents
- Configuration du nombre d'itérations
- Exécution asynchrone (Celery)
- Suivi de l'état des tâches

### 🎨 Interface utilisateur
- Design inspiré de ChatGPT
- Sidebar avec liste de conversations
- Sélection d'agents
- Chat window responsive
- Header avec toggle sidebar

### 🔐 Authentification
- Système de login/logout
- Gestion des permissions
- Multi-utilisateurs
- Session management

### ⚙️ Administration
- Interface Django Admin
- Gestion des utilisateurs
- CRUD agents
- Monitoring des conversations

---

## 📝 Structure de la documentation

Chaque fonctionnalité majeure dispose de :

1. **Documentation technique** (`FEATURE_NAME.md`)
   - Architecture et design
   - API endpoints
   - Schéma de base de données
   - Exemples de code
   - Notes techniques

2. **Guide utilisateur** (`FEATURE_NAME_QUICKSTART.md`)
   - Instructions pas à pas
   - Cas d'usage
   - Astuces et bonnes pratiques
   - Dépannage

3. **Récapitulatif d'implémentation** (`FEATURE_NAME_IMPLEMENTATION_COMPLETE.md`)
   - Statut de l'implémentation
   - Fichiers modifiés
   - Tests effectués
   - Prochaines étapes

---

## 🔗 Autres documentations

### Documentation principale
- **[README.md](../../README.md)** - Introduction générale du projet
- **[QUICKSTART.md](../../QUICKSTART.md)** - Guide de démarrage rapide
- **[CHANGELOG.md](../../CHANGELOG.md)** - Historique des versions

### Documentation API
- **[API.md](../api/API.md)** - Documentation complète de l'API REST

### Documentation d'architecture
- **[Backend Architecture](../architecture/backend/)** - Architecture du backend Django
- **[Frontend Architecture](../architecture/frontend/)** - Architecture du frontend React

### Documentation de configuration
- **[LLM Configuration](../configuration/)** - Configuration des modèles LLM
- **[Deployment](../deployment/)** - Guides de déploiement

### Documentation des corrections
- **[Fixes](../fixes/)** - Historique des corrections et guides de dépannage

---

## 🛠️ Comment contribuer à la documentation

### Ajouter une nouvelle fonctionnalité

1. **Créer les fichiers** :
   ```
   docs/features/
   ├── FEATURE_NAME.md                          # Documentation technique
   ├── FEATURE_NAME_QUICKSTART.md               # Guide utilisateur
   └── FEATURE_NAME_IMPLEMENTATION_COMPLETE.md  # Récapitulatif
   ```

2. **Suivre le template** :
   - Utiliser des emojis pour la lisibilité
   - Inclure des exemples de code
   - Ajouter des captures d'écran si pertinent
   - Documenter tous les endpoints API
   - Lister les dépendances

3. **Mettre à jour l'index** :
   - Ajouter la fonctionnalité dans ce README.md
   - Mettre à jour le CHANGELOG.md
   - Créer un lien depuis le README.md principal

### Standards de documentation

- **Format** : Markdown (.md)
- **Langue** : Français
- **Style** : Clair, concis, avec exemples
- **Emojis** : Utiliser pour améliorer la lisibilité
  - 📚 Documentation
  - 🚀 Démarrage rapide
  - ✅ Complet
  - ⏭️ À faire
  - 🐛 Bug
  - ✨ Nouvelle fonctionnalité
  - 🔧 Amélioration
  - 🔒 Sécurité

---

## 📞 Support

Pour toute question sur la documentation :
- Consultez les fichiers existants pour des exemples
- Vérifiez le CHANGELOG.md pour l'historique
- Consultez les guides de dépannage dans docs/fixes/

---

**Dernière mise à jour** : 7 février 2026  
**Version de la documentation** : 1.1.0
