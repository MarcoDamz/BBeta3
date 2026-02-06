# Backend - Dockerfiles Expliqués

Ce dossier contient plusieurs Dockerfiles pour différents environnements de déploiement.

## 📁 Fichiers Docker

### 1. `Dockerfile` - Développement Local (Docker Compose)
**Usage** : Environnement de développement local avec hot-reload

```bash
docker-compose up --build
```

**Caractéristiques** :
- ✅ Build multi-stage pour optimisation
- ✅ Volume monté pour hot-reload
- ✅ Debug activé
- ✅ PostgreSQL et Redis en local

### 2. `Dockerfile.cloudrun` - Production GCP Cloud Run (Backend API)
**Usage** : Déploiement du backend Django sur Cloud Run

```bash
gcloud builds submit --config=../cloudbuild.yaml
```

**Caractéristiques** :
- ✅ Optimisé pour Cloud Run (port 8080)
- ✅ Gunicorn + Uvicorn pour ASGI
- ✅ Cloud SQL Proxy pour PostgreSQL
- ✅ Connexion sécurisée à Memorystore Redis
- ✅ Migrations automatiques au démarrage
- ✅ Collectstatic automatique

**Variables d'environnement** :
- `PORT` : Port d'écoute (8080 par défaut)
- `CLOUD_RUN_SERVICE` : Détection automatique Cloud Run
- `POSTGRES_HOST` : Chemin Cloud SQL Proxy (`/cloudsql/PROJECT:REGION:INSTANCE`)
- `REDIS_HOST` : IP Memorystore Redis

### 3. `Dockerfile.worker` - Production GCP Cloud Run (Celery Worker)
**Usage** : Déploiement du worker Celery sur Cloud Run

```bash
gcloud builds submit --config=../cloudbuild.yaml
```

**Caractéristiques** :
- ✅ Celery worker pour tâches asynchrones
- ✅ Connexion à Cloud SQL et Redis
- ✅ Concurrency=2 pour Cloud Run
- ✅ Auto-restart en cas d'erreur

**Tâches asynchrones** :
- Génération de titres de conversation (LLM)
- Mode Auto-Chat (conversation entre 2 agents)

## 🔧 Scripts d'Entrée

### `docker-entrypoint.sh` - Local Development
Script de démarrage pour Docker Compose :
1. Attend que PostgreSQL soit prêt
2. Applique les migrations Django
3. Crée le superuser si spécifié
4. Collecte les fichiers statiques
5. Lance Uvicorn avec hot-reload

### `docker-entrypoint-cloudrun.sh` - Cloud Run
Script de démarrage optimisé pour Cloud Run :
1. Vérifie la connexion à Cloud SQL
2. Applique les migrations
3. Crée le superuser si variables définies
4. Collecte les fichiers statiques
5. Lance Gunicorn avec Uvicorn workers

**Configuration Gunicorn** :
- Workers : 2
- Worker class : `uvicorn.workers.UvicornWorker`
- Timeout : 300 secondes
- Bind : `0.0.0.0:${PORT:-8080}`

## 📦 Dépendances

### `requirements.txt`
Dépendances Python communes à tous les environnements :
- Django 5.x
- Django REST Framework
- Celery + Redis
- LangChain (OpenAI, Anthropic)
- PostgreSQL (psycopg2)
- Uvicorn (ASGI)
- Django CORS Headers

**Dépendances supplémentaires Cloud Run** :
- `gunicorn` - Production WSGI/ASGI server
- `gevent` - Async workers

## 🚀 Commandes de Build

### Local (Docker Compose)
```bash
# Depuis la racine du projet
docker-compose up --build

# Rebuild sans cache
docker-compose build --no-cache backend
```

### Cloud Run (Backend)
```bash
# Build et push manuel
cd backend
gcloud builds submit \
  -t gcr.io/PROJECT_ID/chatagentb-backend:latest \
  -f Dockerfile.cloudrun .

# Déployer
gcloud run deploy chatagentb-backend \
  --image gcr.io/PROJECT_ID/chatagentb-backend:latest \
  --region europe-west1
```

### Cloud Run (Worker)
```bash
# Build et push manuel
cd backend
gcloud builds submit \
  -t gcr.io/PROJECT_ID/chatagentb-worker:latest \
  -f Dockerfile.worker .

# Déployer
gcloud run deploy chatagentb-worker \
  --image gcr.io/PROJECT_ID/chatagentb-worker:latest \
  --region europe-west1
```

## 🔍 Différences entre les Dockerfiles

| Aspect | Dockerfile (local) | Dockerfile.cloudrun | Dockerfile.worker |
|--------|-------------------|---------------------|-------------------|
| **Port** | 8000 | 8080 (Cloud Run) | N/A |
| **Server** | Uvicorn | Gunicorn + Uvicorn | Celery |
| **Reload** | ✅ Hot-reload | ❌ Production | ❌ Production |
| **DB** | Local PostgreSQL | Cloud SQL Proxy | Cloud SQL Proxy |
| **Redis** | Local Redis | Memorystore | Memorystore |
| **Env** | DEBUG=True | DEBUG=False | DEBUG=False |
| **Usage** | Développement | API Production | Tasks Production |

## 🔐 Variables d'Environnement

### Communes
```bash
DEBUG=False
SECRET_KEY=your-secret-key
POSTGRES_DB=chatagentb
POSTGRES_USER=chatagentb
POSTGRES_PASSWORD=your-password
REDIS_HOST=redis-ip
CELERY_BROKER_URL=redis://redis-ip:6379/0
OPENAI_API_KEY=sk-your-key
```

### Spécifiques Cloud Run
```bash
PORT=8080  # Automatique sur Cloud Run
CLOUD_RUN_SERVICE=chatagentb-backend  # Automatique
POSTGRES_HOST=/cloudsql/PROJECT:REGION:INSTANCE  # Cloud SQL Proxy
ALLOWED_HOSTS=.run.app,.a.run.app
```

## 📊 Monitoring

### Logs Backend
```bash
# Local
docker-compose logs -f backend

# Cloud Run
gcloud run logs tail --service chatagentb-backend --region europe-west1
```

### Logs Worker
```bash
# Local
docker-compose logs -f worker

# Cloud Run
gcloud run logs tail --service chatagentb-worker --region europe-west1
```

## 🐛 Troubleshooting

### Erreur : Port already in use (local)
```bash
# Trouver le processus
netstat -ano | findstr :8000
# Tuer le processus
taskkill /PID <PID> /F
```

### Erreur : Cannot connect to PostgreSQL (Cloud Run)
```bash
# Vérifier Cloud SQL Proxy
gcloud run services describe chatagentb-backend | grep cloudsql

# Vérifier les permissions
gcloud projects get-iam-policy PROJECT_ID
```

### Erreur : Celery worker not starting
```bash
# Vérifier la connexion Redis
redis-cli -h REDIS_IP ping

# Vérifier les logs
gcloud run logs read --service chatagentb-worker --limit=100
```

## 📚 Documentation

- [Guide complet de déploiement GCP](../DEPLOY_GCP.md)
- [Démarrage rapide GCP](../QUICKSTART_GCP.md)
- [Commandes GCP](../GCP_COMMANDS.md)

---

**Note** : Pour plus de détails sur le déploiement GCP, consultez [GCP_SETUP_COMPLETE.md](../GCP_SETUP_COMPLETE.md)
