# 📋 Changelog - ChatAgentB

## [1.1.0] - 2026-02-07

### ✨ Nouvelles fonctionnalités

#### 🗂️ Système de dossiers pour les conversations
- **Organisez vos conversations** : Créez des dossiers pour classer vos conversations
- **Drag & Drop intuitif** : Déplacez vos conversations par glisser-déposer
- **Arborescence** : Support des dossiers et sous-dossiers (via l'admin)
- **Menu contextuel** : Renommez ou supprimez vos dossiers facilement
- **Zone "Non classées"** : Les conversations sans dossier restent accessibles
- **Compteurs** : Voyez combien de conversations sont dans chaque dossier
- **Expand/Collapse** : Ouvrez ou fermez les dossiers d'un clic
- **Persistence** : Tous les dossiers et classements sont sauvegardés en base de données
- **Multi-utilisateurs** : Chaque utilisateur a ses propres dossiers

### 🔧 Améliorations techniques

#### Backend
- **Nouveau modèle** : `Folder` avec support d'arborescence (parent/enfant)
- **API REST complète** : CRUD complet pour les dossiers
- **Nouvelle action** : `move_to_folder` pour déplacer les conversations
- **Admin Django** : Interface d'administration pour les dossiers
- **Contraintes** : Unicité des noms de dossiers par niveau et utilisateur
- **Migration** : `0002_folder_conversation_folder` appliquée

#### Frontend
- **Nouveau composant** : `FolderTree` pour l'arborescence
- **Sidebar améliorée** : Bouton "Nouveau dossier" et gestion du drag & drop
- **Store Zustand** : État global pour les dossiers avec actions complètes
- **Service API** : Endpoints pour la gestion des dossiers
- **UX améliorée** : Feedback visuel lors du drag & drop

### 📚 Documentation
- ✅ `docs/features/FOLDERS_FEATURE.md` - Documentation technique complète
- ✅ `docs/features/FOLDERS_IMPLEMENTATION_COMPLETE.md` - Récapitulatif de l'implémentation
- ✅ `docs/features/FOLDERS_QUICKSTART.md` - Guide de démarrage rapide

### 🎯 Endpoints ajoutés

```
GET    /api/chat/folders/                             - Liste des dossiers
POST   /api/chat/folders/                             - Créer un dossier
GET    /api/chat/folders/{id}/                        - Détails d'un dossier
PATCH  /api/chat/folders/{id}/                        - Modifier un dossier
DELETE /api/chat/folders/{id}/                        - Supprimer un dossier
POST   /api/chat/folders/reorder/                     - Réorganiser les dossiers
POST   /api/chat/conversations/{id}/move_to_folder/   - Déplacer une conversation
```

---

## [1.0.0] - 2026-02-05

### 🎉 Version initiale

#### Fonctionnalités de base
- ✅ Système de chat avec agents IA multiples
- ✅ Support de plusieurs LLM (OpenAI, Anthropic)
- ✅ Conversations persistantes
- ✅ Mode Auto-Chat (conversation entre 2 agents)
- ✅ Génération automatique de titres
- ✅ Interface style ChatGPT
- ✅ Authentification et permissions
- ✅ Administration Django
- ✅ API REST complète (Django REST Framework)
- ✅ Tâches asynchrones (Celery + Redis)
- ✅ Docker Compose pour le déploiement

#### Stack technique
**Backend** :
- Django 5+
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- LangChain
- Uvicorn

**Frontend** :
- React 18
- Vite
- Tailwind CSS
- Zustand (state management)
- Lucide Icons
- date-fns

**Infrastructure** :
- Docker & Docker Compose
- 5 services : db, redis, backend, worker, frontend

---

## 📖 Format du Changelog

Ce changelog suit les principes de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
et respecte le [Semantic Versioning](https://semver.org/lang/fr/).

### Types de changements
- **✨ Nouvelles fonctionnalités** - Nouvelles features ajoutées
- **🔧 Améliorations** - Améliorations de fonctionnalités existantes
- **🐛 Corrections** - Corrections de bugs
- **🔒 Sécurité** - Correctifs de sécurité
- **⚠️ Deprecated** - Fonctionnalités obsolètes
- **🗑️ Supprimé** - Fonctionnalités supprimées
- **📚 Documentation** - Changements dans la documentation

---

## 🔮 Roadmap

### Version 1.2.0 (À venir)
- [ ] Recherche dans les dossiers
- [ ] Export/Import de conversations
- [ ] Thèmes personnalisables
- [ ] Notifications en temps réel
- [ ] Mode hors ligne

### Version 1.3.0 (Planifié)
- [ ] Partage de conversations
- [ ] Intégration avec d'autres LLM
- [ ] Plugin system
- [ ] API publique
- [ ] Mobile responsive

### Backlog
- Déplacement de dossiers par drag & drop
- Icônes personnalisées pour les dossiers
- Couleurs personnalisées
- Raccourcis clavier
- Mode sombre/clair
- Statistiques d'utilisation
- Gestion des favoris

---

**Dernière mise à jour** : 7 février 2026
