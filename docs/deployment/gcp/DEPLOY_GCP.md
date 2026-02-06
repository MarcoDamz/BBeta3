# 🚀 Guide de Déploiement ChatAgentB sur Google Cloud Platform

Ce guide explique comment déployer ChatAgentB sur GCP avec Cloud Run, Cloud SQL (PostgreSQL) et Memorystore (Redis).

## 📋 Prérequis

### 1. Compte GCP
- Compte Google Cloud Platform actif
- Projet GCP créé (ou en créer un nouveau)
- Facturation activée sur le projet

### 2. Outils Installés
- **Google Cloud SDK** : [Installer gcloud CLI](https://cloud.google.com/sdk/docs/install)
- **Docker** (optionnel, pour tests locaux)
- **PowerShell** (Windows) ou **Bash** (Linux/Mac)

### 3. Configuration Initiale

```powershell
# Installer gcloud CLI
# Windows: https://cloud.google.com/sdk/docs/install

# Authentification
gcloud auth login

# Lister vos projets
gcloud projects list

# Créer un nouveau projet (optionnel)
gcloud projects create mon-chatagentb-project --name="ChatAgentB"

# Définir le projet par défaut
gcloud config set project mon-chatagentb-project
```

## 🏗️ Architecture sur GCP

```
┌─────────────────────────────────────────────────────────┐
│                     Google Cloud                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────┐     ┌────────────────┐             │
│  │   Cloud Run    │     │   Cloud Run    │             │
│  │   (Frontend)   │────▶│   (Backend)    │             │
│  │   Nginx        │     │   Django/DRF   │             │
│  └────────────────┘     └────────┬───────┘             │
│                                   │                      │
│                         ┌─────────┴────────┐            │
│                         │                  │            │
│              ┌──────────▼────────┐  ┌─────▼──────────┐ │
│              │   Cloud SQL       │  │  Memorystore   │ │
│              │   (PostgreSQL)    │  │    (Redis)     │ │
│              └───────────────────┘  └────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │          Cloud Run (Celery Worker)                 │ │
│  │          Tâches asynchrones                        │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │          Secret Manager                            │ │
│  │          (API Keys, Passwords)                     │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Déploiement Automatique (Recommandé)

### Option 1 : Script PowerShell (Windows)

```powershell
# Exécuter le script de déploiement
.\deploy-gcp.ps1 -ProjectId "mon-chatagentb-project" -Region "europe-west1"
```

Le script va :
1. ✅ Activer les APIs nécessaires
2. ✅ Créer les secrets (Django, DB, OpenAI)
3. ✅ Créer Cloud SQL PostgreSQL
4. ✅ Créer Memorystore Redis
5. ✅ Builder et déployer les 3 services (Frontend, Backend, Worker)

### Option 2 : Déploiement Manuel

Si vous préférez contrôler chaque étape :

#### Étape 1 : Activer les APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  sqladmin.googleapis.com \
  redis.googleapis.com \
  secretmanager.googleapis.com \
  containerregistry.googleapis.com
```

#### Étape 2 : Créer les Secrets

```bash
# Secret Key Django (générer une clé aléatoire)
echo "votre-secret-key-django-aleatoire-50-chars" | \
  gcloud secrets create django-secret --data-file=-

# Mot de passe DB
echo "votre-mot-de-passe-db" | \
  gcloud secrets create db-password --data-file=-

# Clé API OpenAI
echo "sk-votre-cle-openai" | \
  gcloud secrets create openai-api-key --data-file=-
```

#### Étape 3 : Créer Cloud SQL

```bash
# Créer l'instance PostgreSQL
gcloud sql instances create chatagentb-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west1 \
  --root-password="votre-mot-de-passe-root" \
  --storage-type=SSD \
  --storage-size=10GB \
  --backup

# Créer la base de données
gcloud sql databases create chatagentb \
  --instance=chatagentb-db

# Créer l'utilisateur
gcloud sql users create chatagentb \
  --instance=chatagentb-db \
  --password="votre-mot-de-passe-db"
```

#### Étape 4 : Créer Redis

```bash
# Créer l'instance Memorystore Redis
gcloud redis instances create chatagentb-redis \
  --size=1 \
  --region=europe-west1 \
  --redis-version=redis_7_0 \
  --tier=basic

# Récupérer l'IP Redis
gcloud redis instances describe chatagentb-redis \
  --region=europe-west1 \
  --format="value(host)"
```

#### Étape 5 : Déployer avec Cloud Build

```bash
# Substituer les variables dans cloudbuild.yaml
export PROJECT_ID="mon-chatagentb-project"
export REGION="europe-west1"
export CLOUDSQL_INSTANCE="${PROJECT_ID}:${REGION}:chatagentb-db"
export REDIS_HOST="10.x.x.x"  # IP de Redis

# Soumettre le build
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=${REGION},_CLOUDSQL_INSTANCE=${CLOUDSQL_INSTANCE},_DB_NAME=chatagentb,_DB_USER=chatagentb,_REDIS_HOST=${REDIS_HOST}
```

## 🔧 Configuration Post-Déploiement

### 1. Configurer le CORS

Mettre à jour `backend/chatagentb/settings.py` :

```python
# Récupérer l'URL du frontend depuis Cloud Run
FRONTEND_URL = "https://chatagentb-frontend-xxx-ew.a.run.app"

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

CSRF_TRUSTED_ORIGINS = [
    FRONTEND_URL,
]
```

### 2. Créer un Superuser

```bash
# Se connecter au container backend
gcloud run services update chatagentb-backend \
  --region=europe-west1 \
  --update-env-vars DJANGO_SUPERUSER_USERNAME=admin,DJANGO_SUPERUSER_EMAIL=admin@example.com,DJANGO_SUPERUSER_PASSWORD=admin123

# Ou via Cloud Shell
gcloud run services proxy chatagentb-backend --region=europe-west1
# Puis dans un autre terminal :
docker exec -it chatagentb-backend python manage.py createsuperuser
```

### 3. Vérifier les Logs

```bash
# Logs Backend
gcloud run logs read --service chatagentb-backend --region=europe-west1

# Logs Worker
gcloud run logs read --service chatagentb-worker --region=europe-west1

# Logs Frontend
gcloud run logs read --service chatagentb-frontend --region=europe-west1
```

## 🔐 Gestion des Secrets

### Mettre à jour un secret

```bash
# Nouvelle version d'un secret
echo "nouvelle-valeur" | gcloud secrets versions add django-secret --data-file=-

# Lister les versions
gcloud secrets versions list django-secret

# Redéployer pour appliquer
gcloud run services update chatagentb-backend --region=europe-west1
```

## 📊 Monitoring et Observabilité

### Cloud Logging

```bash
# Filtrer les logs par niveau
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit 50

# Logs en temps réel
gcloud run logs tail --service chatagentb-backend --region=europe-west1
```

### Cloud Monitoring

1. Accéder à [Cloud Console - Monitoring](https://console.cloud.google.com/monitoring)
2. Créer des dashboards pour :
   - Latence des requêtes
   - Taux d'erreur
   - Utilisation mémoire/CPU
   - Nombre d'instances actives

## 💰 Coûts Estimés

### Configuration Minimale (Tier gratuit partiel)

| Service | Configuration | Coût Mensuel Estimé |
|---------|---------------|---------------------|
| Cloud Run (Backend) | 1-2 instances, 2 vCPU, 2 GB RAM | ~$20-40 |
| Cloud Run (Worker) | 1 instance, 2 vCPU, 2 GB RAM | ~$15-25 |
| Cloud Run (Frontend) | 1-2 instances, 1 vCPU, 512 MB RAM | ~$5-10 |
| Cloud SQL (PostgreSQL) | db-f1-micro, 10 GB SSD | ~$10 |
| Memorystore (Redis) | 1 GB, Basic tier | ~$35 |
| **Total** | | **~$85-120/mois** |

### Optimisations Possibles

- Utiliser le tier gratuit de Cloud Run (2M requêtes/mois)
- Réduire les instances min à 0 en période creuse
- Utiliser Cloud SQL Proxy pour économiser sur les connexions
- Activer l'autoscaling intelligent

## 🔄 CI/CD avec Cloud Build

### Déploiement Automatique depuis GitHub

1. **Connecter votre dépôt GitHub** :
   ```bash
   # Depuis Cloud Console > Cloud Build > Triggers
   # Ou via CLI :
   gcloud builds triggers create github \
     --repo-name=chatagentb \
     --repo-owner=votre-username \
     --branch-pattern="^main$" \
     --build-config=cloudbuild.yaml
   ```

2. **Push sur GitHub déclenche le déploiement** :
   ```bash
   git push origin main
   # Cloud Build détecte le push et déploie automatiquement
   ```

## 🛠️ Maintenance

### Mise à jour de l'application

```bash
# 1. Modifier le code localement
# 2. Commit et push
git add .
git commit -m "Update feature X"
git push origin main

# 3. Cloud Build déploie automatiquement (si trigger configuré)
# Ou manuellement :
gcloud builds submit --config=cloudbuild.yaml
```

### Rollback

```bash
# Lister les révisions
gcloud run revisions list --service chatagentb-backend --region=europe-west1

# Revenir à une révision précédente
gcloud run services update-traffic chatagentb-backend \
  --region=europe-west1 \
  --to-revisions=chatagentb-backend-00005-abc=100
```

### Backup de la base de données

```bash
# Créer un backup manuel
gcloud sql backups create --instance=chatagentb-db

# Lister les backups
gcloud sql backups list --instance=chatagentb-db

# Restaurer depuis un backup
gcloud sql backups restore BACKUP_ID --backup-instance=chatagentb-db --backup-location=europe-west1
```

## 🔧 Troubleshooting

### Problème : Service ne démarre pas

```bash
# Vérifier les logs
gcloud run logs read --service chatagentb-backend --region=europe-west1 --limit=100

# Vérifier les variables d'environnement
gcloud run services describe chatagentb-backend --region=europe-west1 --format=yaml
```

### Problème : Erreur de connexion DB

```bash
# Vérifier que Cloud SQL Proxy est configuré
gcloud run services describe chatagentb-backend --region=europe-west1 | grep cloudsql

# Tester la connexion depuis Cloud Shell
gcloud sql connect chatagentb-db --user=chatagentb
```

### Problème : Erreur de connexion Redis

```bash
# Vérifier l'IP Redis
gcloud redis instances describe chatagentb-redis --region=europe-west1

# Vérifier la configuration réseau (VPC)
gcloud redis instances describe chatagentb-redis --region=europe-west1 --format="value(network)"
```

## 📚 Ressources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Memorystore Documentation](https://cloud.google.com/memorystore/docs/redis)
- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)

## 🎉 Félicitations !

Votre application ChatAgentB est maintenant déployée sur GCP et accessible depuis n'importe où dans le monde ! 🌍

Pour toute question ou problème, consultez les logs ou ouvrez une issue sur GitHub.
