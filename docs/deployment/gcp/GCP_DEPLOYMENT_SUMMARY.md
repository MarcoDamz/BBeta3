# 📦 Résumé de la Configuration GCP pour ChatAgentB

Ce fichier résume tous les éléments créés pour le déploiement sur Google Cloud Platform.

## 📁 Fichiers de Configuration Créés

### 1. Dockerfiles pour Cloud Run

| Fichier | Description |
|---------|-------------|
| `backend/Dockerfile.cloudrun` | Image Docker optimisée pour Cloud Run (Backend Django) |
| `backend/Dockerfile.worker` | Image Docker pour Celery Worker |
| `frontend/Dockerfile.cloudrun` | Image Docker optimisée pour Cloud Run (Frontend React) |

### 2. Scripts d'Entrée

| Fichier | Description |
|---------|-------------|
| `backend/docker-entrypoint-cloudrun.sh` | Script de démarrage backend avec migrations et collectstatic |
| `frontend/docker-entrypoint-cloudrun.sh` | Script de démarrage frontend avec substitution de variables |

### 3. Configuration Nginx

| Fichier | Description |
|---------|-------------|
| `frontend/nginx.cloudrun.conf` | Configuration Nginx pour Cloud Run avec health check |

### 4. Cloud Build

| Fichier | Description |
|---------|-------------|
| `cloudbuild.yaml` | Configuration CI/CD pour Cloud Build (3 services) |

### 5. Scripts de Déploiement

| Fichier | Description |
|---------|-------------|
| `deploy-gcp.ps1` | Script PowerShell pour déploiement automatique (Windows) |
| `deploy-gcp.sh` | Script Bash pour déploiement automatique (Linux/Mac) |

### 6. Optimisation Build

| Fichier | Description |
|---------|-------------|
| `.gcloudignore` | Exclusions pour Cloud Build (racine) |
| `backend/.gcloudignore` | Exclusions pour build backend |
| `frontend/.gcloudignore` | Exclusions pour build frontend |
| `backend/.dockerignore` | Exclusions pour Docker backend |
| `frontend/.dockerignore` | Exclusions pour Docker frontend |

### 7. Documentation

| Fichier | Description |
|---------|-------------|
| `DEPLOY_GCP.md` | Guide complet de déploiement sur GCP (architecture, coûts, troubleshooting) |
| `QUICKSTART_GCP.md` | Guide de démarrage rapide pour déploiement GCP |

### 8. Modifications de Code

| Fichier | Modification |
|---------|--------------|
| `backend/chatagentb/settings.py` | Ajout de la détection Cloud Run (ALLOWED_HOSTS, CORS, CSRF) |
| `README.md` | Section déploiement GCP ajoutée |

## 🏗️ Architecture Cloud Run

```
┌─────────────────────────────────────────────────────────┐
│                   Google Cloud Platform                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐                                   │
│  │   Cloud Run      │     Frontend (React + Nginx)      │
│  │   chatagentb-    │     - Serve fichiers statiques    │
│  │   frontend       │     - Gestion du routing SPA      │
│  └────────┬─────────┘     - Health check endpoint       │
│           │                                              │
│           │  HTTPS                                       │
│           ▼                                              │
│  ┌──────────────────┐                                   │
│  │   Cloud Run      │     Backend (Django + DRF)        │
│  │   chatagentb-    │     - API REST                    │
│  │   backend        │     - Admin Django                │
│  └────┬─────────┬───┘     - Cloud SQL Proxy            │
│       │         │          - Gunicorn + Uvicorn         │
│       │         │                                        │
│       │         └──────────────┐                        │
│       │                        │                        │
│       ▼                        ▼                        │
│  ┌──────────────┐      ┌─────────────────┐            │
│  │  Cloud SQL   │      │  Memorystore    │            │
│  │  PostgreSQL  │      │  Redis          │            │
│  │  15          │      │  7.0            │            │
│  └──────────────┘      └─────────────────┘            │
│       ▲                        ▲                        │
│       │                        │                        │
│       └────────┬───────────────┘                        │
│                │                                         │
│       ┌────────▼─────────┐                             │
│       │   Cloud Run      │     Worker (Celery)          │
│       │   chatagentb-    │     - Tâches asynchrones     │
│       │   worker         │     - Génération de titres   │
│       └──────────────────┘     - Auto-chat             │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │             Secret Manager                        │  │
│  │  - django-secret                                  │  │
│  │  - db-password                                    │  │
│  │  - openai-api-key                                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Commandes de Déploiement

### Déploiement Initial (Automatique)

```powershell
# Windows
.\deploy-gcp.ps1 -ProjectId "mon-projet-gcp" -Region "europe-west1"

# Linux/Mac
chmod +x deploy-gcp.sh
./deploy-gcp.sh mon-projet-gcp europe-west1
```

### Mise à Jour (Manual Build)

```bash
# Définir les variables
export PROJECT_ID="mon-projet-gcp"
export REGION="europe-west1"
export CLOUDSQL_INSTANCE="${PROJECT_ID}:${REGION}:chatagentb-db"
export REDIS_HOST="10.x.x.x"  # Remplacer par l'IP Redis

# Soumettre le build
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=${REGION},_CLOUDSQL_INSTANCE=${CLOUDSQL_INSTANCE},_DB_NAME=chatagentb,_DB_USER=chatagentb,_REDIS_HOST=${REDIS_HOST}
```

### Mise à Jour Rapide (Service Individuel)

```bash
# Backend uniquement
cd backend
gcloud builds submit -t gcr.io/${PROJECT_ID}/chatagentb-backend:latest -f Dockerfile.cloudrun .
gcloud run deploy chatagentb-backend \
  --image gcr.io/${PROJECT_ID}/chatagentb-backend:latest \
  --region ${REGION}

# Frontend uniquement
cd frontend
gcloud builds submit -t gcr.io/${PROJECT_ID}/chatagentb-frontend:latest -f Dockerfile.cloudrun .
gcloud run deploy chatagentb-frontend \
  --image gcr.io/${PROJECT_ID}/chatagentb-frontend:latest \
  --region ${REGION}

# Worker uniquement
cd backend
gcloud builds submit -t gcr.io/${PROJECT_ID}/chatagentb-worker:latest -f Dockerfile.worker .
gcloud run deploy chatagentb-worker \
  --image gcr.io/${PROJECT_ID}/chatagentb-worker:latest \
  --region ${REGION}
```

## 🔐 Gestion des Secrets

### Créer/Mettre à jour un secret

```bash
# Django Secret Key
echo "nouvelle-secret-key-aleatoire-50-chars" | gcloud secrets create django-secret --data-file=-

# Mot de passe DB
echo "nouveau-mot-de-passe-db" | gcloud secrets create db-password --data-file=-

# Clé API OpenAI
echo "sk-nouvelle-cle-openai" | gcloud secrets create openai-api-key --data-file=-
```

### Ajouter une nouvelle version

```bash
# Ajouter une nouvelle version (garde l'historique)
echo "nouvelle-valeur" | gcloud secrets versions add django-secret --data-file=-
```

### Donner accès au service Cloud Run

```bash
# Autoriser Cloud Run à lire les secrets
gcloud secrets add-iam-policy-binding django-secret \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## 📊 Monitoring et Logs

### Voir les logs en temps réel

```bash
# Backend
gcloud run logs tail --service chatagentb-backend --region ${REGION}

# Worker
gcloud run logs tail --service chatagentb-worker --region ${REGION}

# Frontend
gcloud run logs tail --service chatagentb-frontend --region ${REGION}
```

### Logs avec filtre

```bash
# Erreurs uniquement
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit 50

# Logs d'une requête spécifique
gcloud logging read "resource.type=cloud_run_revision AND textPayload:'/api/agents/'" --limit 20
```

### Métriques

```bash
# Nombre de requêtes
gcloud monitoring time-series list \
  --filter='resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_count"'

# Latence
gcloud monitoring time-series list \
  --filter='resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_latencies"'
```

## 💰 Estimation des Coûts (Mensuels)

### Configuration Standard

| Service | Tier | vCPU | Mémoire | Instances | Coût/mois |
|---------|------|------|---------|-----------|-----------|
| Backend (Cloud Run) | - | 2 | 2 GB | 1-10 | ~$30-40 |
| Worker (Cloud Run) | - | 2 | 2 GB | 1-5 | ~$20-25 |
| Frontend (Cloud Run) | - | 1 | 512 MB | 1-10 | ~$8-12 |
| Cloud SQL | db-f1-micro | 1 | 3.75 GB | 1 | ~$10 |
| Memorystore Redis | Basic | - | 1 GB | 1 | ~$35 |
| **Total** | | | | | **~$103-122** |

### Optimisations Possibles

1. **Réduire les instances min à 0** (cold start possible)
   ```bash
   gcloud run services update chatagentb-backend --min-instances=0
   ```

2. **Utiliser Cloud SQL Proxy Serverless**
   ```bash
   # Évite les frais de connexion permanente
   # Déjà configuré dans cloudbuild.yaml avec --set-cloudsql-instances
   ```

3. **Activer l'autoscaling agressif**
   ```bash
   gcloud run services update chatagentb-backend \
     --max-instances=5 \
     --concurrency=80
   ```

## 🔄 CI/CD avec GitHub

### Configurer le déploiement automatique

1. **Créer un trigger Cloud Build** :
   ```bash
   gcloud builds triggers create github \
     --repo-name=chatagentb \
     --repo-owner=votre-username \
     --branch-pattern="^main$" \
     --build-config=cloudbuild.yaml
   ```

2. **Push vers GitHub déclenche le déploiement** :
   ```bash
   git push origin main
   # Cloud Build détecte automatiquement et déploie
   ```

## 🛠️ Maintenance

### Backup de la base de données

```bash
# Créer un backup manuel
gcloud sql backups create --instance=chatagentb-db

# Lister les backups
gcloud sql backups list --instance=chatagentb-db

# Restaurer depuis un backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=chatagentb-db \
  --backup-location=europe-west1
```

### Mise à l'échelle manuelle

```bash
# Augmenter les instances backend
gcloud run services update chatagentb-backend \
  --min-instances=2 \
  --max-instances=20 \
  --region ${REGION}

# Augmenter la mémoire
gcloud run services update chatagentb-backend \
  --memory=4Gi \
  --region ${REGION}
```

### Rollback

```bash
# Lister les révisions
gcloud run revisions list --service chatagentb-backend --region ${REGION}

# Revenir à une révision précédente
gcloud run services update-traffic chatagentb-backend \
  --to-revisions=chatagentb-backend-00005-abc=100 \
  --region ${REGION}
```

## 🐛 Troubleshooting Rapide

### Service ne démarre pas

```bash
# Vérifier les logs
gcloud run logs read --service chatagentb-backend --limit=100

# Vérifier la configuration
gcloud run services describe chatagentb-backend --format=yaml
```

### Erreur de connexion DB

```bash
# Vérifier Cloud SQL Proxy
gcloud run services describe chatagentb-backend | grep cloudsql

# Tester la connexion
gcloud sql connect chatagentb-db --user=chatagentb
```

### Erreur 502 Bad Gateway

```bash
# Vérifier que le service écoute sur le bon port (8080)
# Vérifier la variable PORT dans le Dockerfile
```

## 📚 Ressources Utiles

- [Documentation GCP complète](./DEPLOY_GCP.md)
- [Guide de démarrage rapide](./QUICKSTART_GCP.md)
- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Cloud SQL Docs](https://cloud.google.com/sql/docs)
- [Secret Manager Docs](https://cloud.google.com/secret-manager/docs)

---

**Dernière mise à jour** : Janvier 2026  
**Version** : 1.0.0  
**Support** : Voir [DEPLOY_GCP.md](./DEPLOY_GCP.md) pour assistance
