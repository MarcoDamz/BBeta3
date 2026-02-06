# 🚀 Déploiement Rapide sur GCP Cloud Run

Guide de démarrage rapide pour déployer ChatAgentB sur Google Cloud Platform.

## ⚡ Déploiement en 3 Commandes

### Prérequis (5 minutes)

1. **Installer Google Cloud SDK** :
   - Windows : [Installer gcloud CLI](https://cloud.google.com/sdk/docs/install)
   - Mac : `brew install --cask google-cloud-sdk`
   - Linux : `curl https://sdk.cloud.google.com | bash`

2. **Authentification** :
   ```bash
   gcloud auth login
   gcloud config set project VOTRE_PROJECT_ID
   ```

3. **Activer la facturation** sur votre projet GCP

### Déploiement Automatique (15-20 minutes)

#### Windows (PowerShell)

```powershell
.\deploy-gcp.ps1 -ProjectId "mon-chatagentb-project" -Region "europe-west1"
```

#### Linux/Mac (Bash)

```bash
chmod +x deploy-gcp.sh
./deploy-gcp.sh mon-chatagentb-project europe-west1
```

**Le script va** :
- ✅ Activer les APIs nécessaires
- ✅ Créer les secrets (vous demandera les mots de passe)
- ✅ Créer Cloud SQL PostgreSQL (10 GB)
- ✅ Créer Memorystore Redis (1 GB)
- ✅ Builder et déployer 3 services Cloud Run
- ✅ Afficher les URLs d'accès

### Accéder à votre application

Une fois le déploiement terminé, le script affichera :

```
🌐 URLs de l'application:
  Backend:  https://chatagentb-backend-xxx-ew.a.run.app
  Frontend: https://chatagentb-frontend-xxx-ew.a.run.app
  Admin:    https://chatagentb-backend-xxx-ew.a.run.app/admin/
```

## 🔧 Configuration Post-Déploiement

### 1. Créer un Superuser

```bash
# Mettre à jour les variables d'environnement
gcloud run services update chatagentb-backend \
  --region=europe-west1 \
  --update-env-vars \
  DJANGO_SUPERUSER_USERNAME=admin,\
  DJANGO_SUPERUSER_EMAIL=admin@example.com,\
  DJANGO_SUPERUSER_PASSWORD=VotreMotDePasseSecurise

# Redémarrer le service pour appliquer
gcloud run services update chatagentb-backend --region=europe-west1
```

### 2. Configurer le Frontend

Récupérez l'URL du backend et mettez à jour le frontend :

```bash
# Récupérer l'URL backend
BACKEND_URL=$(gcloud run services describe chatagentb-backend --region=europe-west1 --format="value(status.url)")

# Redéployer le frontend avec la bonne URL
gcloud builds submit ./frontend \
  --config=cloudbuild-frontend.yaml \
  --substitutions=_BACKEND_URL=$BACKEND_URL
```

### 3. Vérifier le déploiement

```bash
# Logs backend
gcloud run logs read --service chatagentb-backend --region=europe-west1 --limit=50

# Tester l'API
curl https://chatagentb-backend-xxx-ew.a.run.app/api/agents/

# Accéder au frontend
open https://chatagentb-frontend-xxx-ew.a.run.app
```

## 📊 Architecture Déployée

```
┌─────────────────────────────────────┐
│    Cloud Run (Frontend)             │
│    https://*.run.app                │
│    Nginx + React                    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│    Cloud Run (Backend)              │
│    https://*.run.app                │
│    Django + DRF + Gunicorn          │
└──────┬────────────┬─────────────────┘
       │            │
       ▼            ▼
┌──────────┐  ┌────────────┐  ┌──────────────┐
│ Cloud SQL│  │Memorystore │  │  Cloud Run   │
│PostgreSQL│  │   Redis    │  │ Celery Worker│
└──────────┘  └────────────┘  └──────────────┘
```

## 💰 Coûts Estimés

| Service | Config | Coût/mois |
|---------|--------|-----------|
| Backend (Cloud Run) | 2 vCPU, 2 GB | ~$30 |
| Worker (Cloud Run) | 2 vCPU, 2 GB | ~$20 |
| Frontend (Cloud Run) | 1 vCPU, 512 MB | ~$8 |
| Cloud SQL | db-f1-micro, 10 GB | ~$10 |
| Memorystore Redis | 1 GB Basic | ~$35 |
| **Total** | | **~$103/mois** |

**Note** : Cloud Run offre 2M requêtes gratuites/mois sur le tier gratuit.

## 🔄 Mises à Jour

### Déployer une nouvelle version

```bash
# Méthode 1 : Via Cloud Build (recommandé)
gcloud builds submit --config=cloudbuild.yaml

# Méthode 2 : Push sur GitHub (si trigger configuré)
git push origin main
```

### Rollback rapide

```bash
# Lister les révisions
gcloud run revisions list --service chatagentb-backend --region=europe-west1

# Revenir à la version précédente
gcloud run services update-traffic chatagentb-backend \
  --to-revisions=chatagentb-backend-00005-abc=100 \
  --region=europe-west1
```

## 🛠️ Commandes Utiles

### Logs en temps réel

```bash
# Backend
gcloud run logs tail --service chatagentb-backend --region=europe-west1

# Worker
gcloud run logs tail --service chatagentb-worker --region=europe-west1
```

### Shell Django

```bash
# Ouvrir un shell Django
gcloud run services proxy chatagentb-backend --region=europe-west1 &
sleep 5
curl http://localhost:8080/admin/
```

### Backup DB

```bash
# Créer un backup
gcloud sql backups create --instance=chatagentb-db

# Lister les backups
gcloud sql backups list --instance=chatagentb-db
```

## 🔐 Sécurité

### Mettre à jour les secrets

```bash
# Nouvelle clé API OpenAI
echo "sk-nouvelle-cle" | gcloud secrets versions add openai-api-key --data-file=-

# Appliquer les changements
gcloud run services update chatagentb-backend --region=europe-west1
```

### Restreindre l'accès

```bash
# Rendre le backend privé (accessible uniquement par le frontend)
gcloud run services update chatagentb-backend \
  --no-allow-unauthenticated \
  --region=europe-west1

# Configurer IAM pour autoriser le frontend
# (nécessite configuration supplémentaire)
```

## 🐛 Troubleshooting

### Service ne démarre pas

```bash
# Vérifier les logs
gcloud run logs read --service chatagentb-backend --region=europe-west1 --limit=100

# Vérifier la config
gcloud run services describe chatagentb-backend --region=europe-west1
```

### Erreur 502 Bad Gateway

```bash
# Vérifier que le service écoute sur le bon port (8080)
# Cloud Run attend le port dans la variable $PORT

# Vérifier les health checks
curl https://chatagentb-backend-xxx.run.app/admin/login/
```

### Erreur de connexion DB

```bash
# Vérifier Cloud SQL Proxy
gcloud run services describe chatagentb-backend --region=europe-west1 | grep cloudsql

# Tester la connexion
gcloud sql connect chatagentb-db --user=chatagentb
```

## 📚 Ressources

- [Documentation complète](./DEPLOY_GCP.md)
- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Cloud SQL Docs](https://cloud.google.com/sql/docs)

## 🎉 C'est Parti !

Votre application est maintenant en ligne et accessible depuis n'importe où ! 🌍

```bash
# Ouvrir l'application
open https://chatagentb-frontend-xxx.run.app
```

**Questions ?** Consultez [DEPLOY_GCP.md](./DEPLOY_GCP.md) pour plus de détails.
