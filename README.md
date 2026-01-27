# ChatAgentB - Chatbot IA Multi-Agents 🤖

Application de Chatbot IA multi-agents permettant de discuter avec des agents configurables et de simuler des conv2. Renseigner :
   - **Nom** : Ex. "Assistant Python"
   - **Modèle LLM** : Choisir azure.gpt-4.1, azure.gpt-4o, azure.gpt-5.1-turbo
   - **System Prompt** : Instructions pour l'agenttions automatiques entre deux agents.

## 🚀 Stack Technique

### Backend
- **Django 5+** - Framework web Python
- **Django REST Framework (DRF)** - API RESTful
- **Uvicorn** - Serveur ASGI haute performance
- **Celery** - Gestion des tâches asynchrones
- **Redis** - Broker pour Celery
- **LangChain** - Orchestration des LLM
- **PostgreSQL** - Base de données relationnelle

### Frontend
- **React 18** - Framework JavaScript
- **Tailwind CSS** - Design moderne type ChatGPT
- **Zustand** - Gestion d'état
- **Vite** - Build tool rapide
- **Axios** - Client HTTP

### Infrastructure
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration multi-conteneurs
- **Nginx** - Serveur web pour le frontend

## 📋 Fonctionnalités

### 1. Gestion des Agents
- ✅ CRUD complet des agents IA
- ✅ Configuration LLM (azure.gpt-4.1, azure.gpt-4o, azure.gpt-5.1-turbo)
- ✅ System prompts personnalisables
- ✅ Paramètres ajustables (température, max_tokens)
- ✅ Système de tags/catégories
- ✅ Duplication d'agents
- ✅ Restriction d'accès (admin uniquement)

### 2. Conversations
- ✅ Interface de chat en temps réel
- ✅ Historique des conversations
- ✅ Génération automatique de titres (via IA)
- ✅ Sélection d'agent dynamique
- ✅ Gestion multi-utilisateurs

### 3. Mode Auto-Chat
- ✅ Conversation automatique entre 2 agents
- ✅ Configuration du nombre d'itérations
- ✅ Traitement asynchrone (Celery)
- ✅ Enregistrement avec préfixe "AUTO:"
- ✅ Accès admin uniquement

## 🏗️ Architecture

```
BBeta3/
├── backend/                    # Backend Django
│   ├── chatagentb/            # Configuration projet
│   │   ├── settings.py        # Configuration Django
│   │   ├── celery.py          # Configuration Celery
│   │   ├── urls.py            # Routes principales
│   │   └── asgi.py            # Configuration ASGI
│   ├── agents/                # App gestion agents
│   │   ├── models.py          # Modèle Agent
│   │   ├── serializers.py     # Serializers DRF
│   │   ├── views.py           # ViewSets API
│   │   └── urls.py            # Routes agents
│   ├── chat/                  # App conversations
│   │   ├── models.py          # Modèles Conversation, Message
│   │   ├── serializers.py     # Serializers DRF
│   │   ├── views.py           # ViewSets API
│   │   ├── tasks.py           # Tâches Celery
│   │   ├── llm_service.py     # Service LangChain
│   │   └── urls.py            # Routes chat
│   ├── requirements.txt       # Dépendances Python
│   ├── Dockerfile             # Image Docker backend
│   └── docker-entrypoint.sh   # Script de démarrage
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── components/        # Composants React
│   │   │   ├── Sidebar.jsx    # Barre latérale
│   │   │   ├── Header.jsx     # En-tête avec sélecteur
│   │   │   ├── ChatWindow.jsx # Zone de chat
│   │   │   └── ChatInput.jsx  # Input utilisateur
│   │   ├── pages/
│   │   │   ├── ChatPage.jsx   # Page principale
│   │   │   └── AdminPage.jsx  # Page admin
│   │   ├── services/
│   │   │   └── api.js         # Client API
│   │   ├── store/
│   │   │   └── useStore.js    # Store Zustand
│   │   ├── App.jsx            # Composant racine
│   │   └── main.jsx           # Point d'entrée
│   ├── package.json           # Dépendances npm
│   ├── Dockerfile             # Image Docker frontend
│   └── nginx.conf             # Configuration Nginx
├── docker-compose.yml          # Orchestration Docker
├── .env.example               # Template variables d'environnement
└── README.md                  # Documentation
```

## 🚦 Installation et Démarrage

### Prérequis
- Docker Desktop (Windows/Mac) ou Docker Engine + Docker Compose (Linux)
- Clé API OpenAI

### 1. Cloner et Configurer

```powershell
# Cloner le dépôt (si depuis Git)
git clone <repository-url>
cd BBeta3

# Copier le fichier d'environnement
cp .env.example .env
```

### 2. Configurer les Variables d'Environnement

Éditer le fichier `.env` et **OBLIGATOIREMENT** renseigner votre clé API :

```env
# OBLIGATOIRE - Remplacer par votre vraie clé
OPENAI_API_KEY=sk-your-real-openai-key-here

# OPTIONNEL - URL de base personnalisée pour l'API OpenAI
# Laissez vide pour utiliser l'API officielle OpenAI
# Utile pour : proxies, Azure OpenAI, endpoints personnalisés
OPENAI_API_BASE=
```

# Optionnel - Modifier si besoin
POSTGRES_PASSWORD=your-secure-password
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=your-secure-password
```

### 3. Lancer l'Application

```powershell
# Construire et démarrer tous les services
docker-compose up --build

# Ou en mode détaché (arrière-plan)
docker-compose up -d --build
```

### 4. Accéder à l'Application

- **Frontend (Interface utilisateur)** : http://localhost:3000
- **Backend API (Documentation)** : http://localhost:8000/api/
- **Admin Django** : http://localhost:8000/admin/

### 5. Identifiants par Défaut

- **Username** : `admin`
- **Password** : `admin123` (ou celui défini dans `.env`)

## 🎯 Utilisation

### Configuration des Agents

1. Accéder à la page Admin via le bouton "Admin Config"
2. Cliquer sur "Nouvel Agent"
3. Renseigner :
   - **Nom** : Ex. "Assistant Python"
   - **Modèle LLM** : Choisir azure.gpt-4.1, Claude 3, etc.
   - **System Prompt** : Instructions pour l'agent
   - **Température** : 0.0 (déterministe) à 1.0 (créatif)
   - **Max Tokens** : Limite de la réponse
4. Sauvegarder

### Chat avec un Agent

1. Retourner sur la page principale
2. Sélectionner un agent dans le header
3. Taper votre message et appuyer sur "Envoyer"
4. L'historique est sauvegardé automatiquement
5. Le titre de la conversation est généré par IA

### Mode Auto-Chat (Admin uniquement)

1. Page Admin → Bouton "Mode Auto-Chat"
2. Sélectionner Agent A et Agent B
3. Saisir le message initial
4. Définir le nombre d'itérations (1-50)
5. Lancer → La tâche s'exécute en arrière-plan
6. Consulter le résultat dans l'historique (titre "AUTO: Agent A ↔ Agent B")

## 🛠️ Commandes Utiles

### Docker

```powershell
# Voir les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f worker

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (réinitialisation complète)
docker-compose down -v

# Reconstruire un service spécifique
docker-compose up -d --build backend
```

### Django (dans le conteneur backend)

```powershell
# Accéder au shell Django
docker-compose exec backend python manage.py shell

# Créer des migrations
docker-compose exec backend python manage.py makemigrations

# Appliquer les migrations
docker-compose exec backend python manage.py migrate

# Créer un superutilisateur manuellement
docker-compose exec backend python manage.py createsuperuser

# Collecter les fichiers statiques
docker-compose exec backend python manage.py collectstatic --noinput
```

### Celery

```powershell
# Voir les workers actifs
docker-compose exec worker celery -A chatagentb inspect active

# Voir les tâches en attente
docker-compose exec worker celery -A chatagentb inspect scheduled

# Purger toutes les tâches
docker-compose exec worker celery -A chatagentb purge
```

## ⚙️ Configuration Avancée

### URL de Base Personnalisée (OPENAI_API_BASE)

La variable `OPENAI_API_BASE` permet de spécifier un endpoint personnalisé pour l'API OpenAI. Elle est optionnelle.

#### Cas d'usage :

1. **Azure OpenAI Service** :
   ```env
   OPENAI_API_BASE=https://your-resource.openai.azure.com/openai/deployments/your-deployment
   ```

2. **Proxy d'entreprise** :
   ```env
   OPENAI_API_BASE=https://proxy.votre-entreprise.com/openai/v1
   ```

3. **Endpoint personnalisé** (compatible OpenAI) :
   ```env
   OPENAI_API_BASE=https://api.votre-llm.com/v1
   ```

4. **API OpenAI officielle** (par défaut) :
   ```env
   OPENAI_API_BASE=
   # ou
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

**Note** : Laissez vide pour utiliser automatiquement l'API officielle OpenAI.

## 🔐 Sécurité

### En Production

1. **Variables d'environnement** :
   ```env
   DEBUG=False
   SECRET_KEY=<générer une clé sécurisée : python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
   ALLOWED_HOSTS=votre-domaine.com
   ```

2. **Base de données** :
   - Utiliser un mot de passe fort
   - Activer SSL/TLS
   - Sauvegardes régulières

3. **CORS** :
   ```env
   CORS_ALLOWED_ORIGINS=https://votre-domaine.com
   ```

4. **HTTPS** :
   - Configurer un reverse proxy (Nginx/Traefik)
   - Certificat SSL (Let's Encrypt)

## 🌐 Déploiement GCP

### Cloud Run + Cloud SQL

1. **Cloud SQL** :
   ```bash
   gcloud sql instances create chatagentb-db \
     --database-version=POSTGRES_15 \
     --tier=db-f1-micro \
     --region=europe-west1
   ```

2. **Container Registry** :
   ```bash
   docker tag chatagentb-backend gcr.io/PROJECT_ID/chatagentb-backend
   docker push gcr.io/PROJECT_ID/chatagentb-backend
   ```

3. **Cloud Run** :
   ```bash
   gcloud run deploy chatagentb-backend \
     --image gcr.io/PROJECT_ID/chatagentb-backend \
     --add-cloudsql-instances PROJECT_ID:europe-west1:chatagentb-db \
     --set-env-vars POSTGRES_HOST=/cloudsql/PROJECT_ID:europe-west1:chatagentb-db
   ```

## 📊 API Endpoints

### Agents

- `GET /api/agents/` - Liste des agents
- `GET /api/agents/{id}/` - Détails d'un agent
- `POST /api/agents/` - Créer un agent (admin)
- `PUT /api/agents/{id}/` - Modifier un agent (admin)
- `DELETE /api/agents/{id}/` - Supprimer un agent (admin)
- `POST /api/agents/{id}/duplicate/` - Dupliquer un agent (admin)

### Conversations

- `GET /api/chat/conversations/` - Liste des conversations
- `GET /api/chat/conversations/{id}/` - Détails d'une conversation
- `POST /api/chat/conversations/` - Créer une conversation
- `DELETE /api/chat/conversations/{id}/` - Supprimer une conversation
- `POST /api/chat/conversations/send_message/` - Envoyer un message
- `POST /api/chat/conversations/auto_chat/` - Lancer un auto-chat (admin)

### Messages

- `GET /api/chat/messages/` - Liste des messages
- `GET /api/chat/messages/{id}/` - Détails d'un message

## 🧪 Tests

```powershell
# Tests Django
docker-compose exec backend python manage.py test

# Tests avec couverture
docker-compose exec backend coverage run --source='.' manage.py test
docker-compose exec backend coverage report
```

## 🐛 Dépannage

### Problème : Le backend ne démarre pas

```powershell
# Vérifier les logs
docker-compose logs backend

# Recréer la base de données
docker-compose down -v
docker-compose up -d db
docker-compose up backend
```

### Problème : Celery ne traite pas les tâches

```powershell
# Vérifier que Redis fonctionne
docker-compose exec redis redis-cli ping
# Réponse attendue: PONG

# Redémarrer le worker
docker-compose restart worker
```

### Problème : Erreur "LLM API Key not found"

- Vérifier que les clés API sont bien dans `.env`
- Redémarrer les services : `docker-compose restart`

## 📝 TODO / Améliorations Futures

- [ ] Authentification JWT pour le frontend
- [ ] Support des fichiers (upload de documents)
- [ ] Export des conversations (PDF, Markdown)
- [ ] Streaming des réponses LLM (SSE)
- [ ] Analytics et tableaux de bord
- [ ] Tests unitaires et d'intégration
- [ ] CI/CD (GitHub Actions)
- [ ] Multi-langue (i18n)

## 📄 Licence

Ce projet est sous licence MIT.

## 👨‍💻 Auteur

Développé pour démonstration d'architecture moderne avec Django, React, Celery, LangChain et Docker.

---

**Note** : Ce projet nécessite une clé API OpenAI pour fonctionner. Les modèles LLM génèrent des coûts selon votre utilisation.
