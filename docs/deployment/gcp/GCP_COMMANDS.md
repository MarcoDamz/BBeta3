# 🛠️ Commandes GCP Courantes pour ChatAgentB

Guide de référence rapide des commandes les plus utilisées pour gérer ChatAgentB sur GCP.

## 🔧 Configuration Initiale

### Authentification et Projet

```bash
# Se connecter à GCP
gcloud auth login

# Lister les projets
gcloud projects list

# Définir le projet par défaut
gcloud config set project mon-chatagentb-project

# Vérifier la configuration actuelle
gcloud config list

# Définir la région par défaut
gcloud config set run/region europe-west1
```

## 🚀 Déploiement et Build

### Build et Déploiement Complet

```bash
# Déploiement complet via Cloud Build
gcloud builds submit --config=cloudbuild.yaml

# Build avec substitutions personnalisées
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=europe-west1,_DB_NAME=chatagentb
```

### Déploiement d'un Service Individuel

```bash
# Backend uniquement
cd backend
gcloud run deploy chatagentb-backend \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated

# Frontend uniquement
cd frontend
gcloud run deploy chatagentb-frontend \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated

# Worker uniquement
cd backend
gcloud run deploy chatagentb-worker \
  --source . \
  --region europe-west1
```

## 📊 Gestion des Services Cloud Run

### Lister et Décrire

```bash
# Lister tous les services Cloud Run
gcloud run services list --region europe-west1

# Détails d'un service
gcloud run services describe chatagentb-backend --region europe-west1

# Obtenir l'URL d'un service
gcloud run services describe chatagentb-backend \
  --region europe-west1 \
  --format="value(status.url)"

# Lister toutes les révisions d'un service
gcloud run revisions list --service chatagentb-backend --region europe-west1
```

### Mise à Jour de Configuration

```bash
# Mettre à jour les variables d'environnement
gcloud run services update chatagentb-backend \
  --region europe-west1 \
  --update-env-vars DEBUG=False,NEW_VAR=value

# Mettre à jour la mémoire et CPU
gcloud run services update chatagentb-backend \
  --region europe-west1 \
  --memory 4Gi \
  --cpu 2

# Mettre à jour le nombre d'instances
gcloud run services update chatagentb-backend \
  --region europe-west1 \
  --min-instances 0 \
  --max-instances 10

# Mettre à jour le timeout
gcloud run services update chatagentb-backend \
  --region europe-west1 \
  --timeout 600
```

### Gestion du Trafic (Rollback)

```bash
# Diriger 100% du trafic vers une révision spécifique
gcloud run services update-traffic chatagentb-backend \
  --to-revisions chatagentb-backend-00005-abc=100 \
  --region europe-west1

# Split de trafic (canary deployment)
gcloud run services update-traffic chatagentb-backend \
  --to-revisions chatagentb-backend-00006-def=90,chatagentb-backend-00005-abc=10 \
  --region europe-west1
```

### Suppression

```bash
# Supprimer un service
gcloud run services delete chatagentb-backend --region europe-west1

# Supprimer une révision spécifique
gcloud run revisions delete chatagentb-backend-00005-abc --region europe-west1
```

## 📝 Logs et Monitoring

### Logs en Temps Réel

```bash
# Logs backend en temps réel
gcloud run logs tail --service chatagentb-backend --region europe-west1

# Logs avec filtre
gcloud run logs read \
  --service chatagentb-backend \
  --region europe-west1 \
  --limit 100 \
  --format "table(timestamp,severity,textPayload)"

# Logs d'erreur uniquement
gcloud logging read \
  "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit 50 \
  --format json
```

### Recherche de Logs

```bash
# Rechercher dans les logs
gcloud logging read \
  "resource.type=cloud_run_revision AND textPayload=~'/api/agents/'" \
  --limit 20

# Logs entre deux dates
gcloud logging read \
  "resource.type=cloud_run_revision" \
  --start-time "2026-01-01T00:00:00Z" \
  --end-time "2026-01-27T23:59:59Z"
```

## 🗄️ Gestion Cloud SQL

### Instances

```bash
# Lister les instances Cloud SQL
gcloud sql instances list

# Détails d'une instance
gcloud sql instances describe chatagentb-db

# Démarrer/Arrêter une instance
gcloud sql instances patch chatagentb-db --activation-policy ALWAYS
gcloud sql instances patch chatagentb-db --activation-policy NEVER

# Se connecter à l'instance
gcloud sql connect chatagentb-db --user=chatagentb
```

### Bases de Données

```bash
# Lister les bases de données
gcloud sql databases list --instance=chatagentb-db

# Créer une base de données
gcloud sql databases create nouvelle-db --instance=chatagentb-db

# Supprimer une base de données
gcloud sql databases delete ancienne-db --instance=chatagentb-db
```

### Utilisateurs

```bash
# Lister les utilisateurs
gcloud sql users list --instance=chatagentb-db

# Créer un utilisateur
gcloud sql users create nouvel-user \
  --instance=chatagentb-db \
  --password=mot-de-passe

# Changer le mot de passe
gcloud sql users set-password chatagentb \
  --instance=chatagentb-db \
  --password=nouveau-mot-de-passe
```

### Backups

```bash
# Créer un backup manuel
gcloud sql backups create --instance=chatagentb-db

# Lister les backups
gcloud sql backups list --instance=chatagentb-db

# Restaurer depuis un backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=chatagentb-db \
  --backup-location=europe-west1

# Créer un backup automatisé
gcloud sql instances patch chatagentb-db \
  --backup-start-time=03:00
```

## 💾 Gestion Memorystore Redis

### Instances

```bash
# Lister les instances Redis
gcloud redis instances list --region europe-west1

# Détails d'une instance
gcloud redis instances describe chatagentb-redis --region europe-west1

# Obtenir l'IP Redis
gcloud redis instances describe chatagentb-redis \
  --region europe-west1 \
  --format="value(host)"

# Mettre à jour la taille
gcloud redis instances update chatagentb-redis \
  --region europe-west1 \
  --size=2
```

## 🔐 Gestion des Secrets

### Créer et Gérer

```bash
# Créer un secret
echo "valeur-secrete" | gcloud secrets create mon-secret --data-file=-

# Lister les secrets
gcloud secrets list

# Ajouter une nouvelle version
echo "nouvelle-valeur" | gcloud secrets versions add mon-secret --data-file=-

# Lire la dernière version
gcloud secrets versions access latest --secret=mon-secret

# Lire une version spécifique
gcloud secrets versions access 2 --secret=mon-secret

# Supprimer un secret
gcloud secrets delete mon-secret
```

### Permissions

```bash
# Donner accès à un service account
gcloud secrets add-iam-policy-binding mon-secret \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Lister les permissions
gcloud secrets get-iam-policy mon-secret
```

## 🏗️ Gestion Cloud Build

### Builds

```bash
# Lister les builds
gcloud builds list --limit 10

# Détails d'un build
gcloud builds describe BUILD_ID

# Logs d'un build
gcloud builds log BUILD_ID

# Annuler un build en cours
gcloud builds cancel BUILD_ID
```

### Triggers

```bash
# Lister les triggers
gcloud builds triggers list

# Créer un trigger GitHub
gcloud builds triggers create github \
  --repo-name=chatagentb \
  --repo-owner=votre-username \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml

# Exécuter manuellement un trigger
gcloud builds triggers run TRIGGER_ID --branch=main

# Supprimer un trigger
gcloud builds triggers delete TRIGGER_ID
```

## 📦 Gestion des Images Container

### Container Registry (GCR)

```bash
# Lister les images
gcloud container images list --repository=gcr.io/PROJECT_ID

# Lister les tags d'une image
gcloud container images list-tags gcr.io/PROJECT_ID/chatagentb-backend

# Supprimer une image
gcloud container images delete gcr.io/PROJECT_ID/chatagentb-backend:TAG

# Supprimer les images non taguées
gcloud container images list-tags gcr.io/PROJECT_ID/chatagentb-backend \
  --filter='-tags:*' \
  --format='get(digest)' \
  --limit=unlimited | \
  xargs -I {} gcloud container images delete gcr.io/PROJECT_ID/chatagentb-backend@{} --quiet
```

## 💰 Facturation et Quotas

### Facturation

```bash
# Lister les comptes de facturation
gcloud billing accounts list

# Voir les coûts du projet (nécessite billing API)
gcloud billing projects describe PROJECT_ID

# Créer un budget
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="ChatAgentB Budget" \
  --budget-amount=150USD
```

### Quotas

```bash
# Voir les quotas Cloud Run
gcloud compute project-info describe \
  --project=PROJECT_ID \
  --format="value(quotas)"

# Demander une augmentation de quota
# (via Console GCP > IAM & Admin > Quotas)
```

## 🛠️ Commandes de Diagnostic

### Health Checks

```bash
# Vérifier qu'un service répond
curl -I https://chatagentb-backend-xxx.run.app

# Tester l'API
curl https://chatagentb-backend-xxx.run.app/api/agents/

# Vérifier les headers
curl -v https://chatagentb-backend-xxx.run.app
```

### Debug

```bash
# Obtenir les détails d'une erreur de déploiement
gcloud run services describe chatagentb-backend \
  --region europe-west1 \
  --format yaml

# Vérifier la configuration réseau
gcloud compute networks list
gcloud compute networks describe default

# Vérifier les IAM policies
gcloud projects get-iam-policy PROJECT_ID
```

## 📋 Scripts Utiles

### Script de Santé (Health Check)

```bash
#!/bin/bash
# health-check.sh

BACKEND_URL="https://chatagentb-backend-xxx.run.app"
FRONTEND_URL="https://chatagentb-frontend-xxx.run.app"

echo "🔍 Vérification de la santé des services..."

# Backend
if curl -s -o /dev/null -w "%{http_code}" $BACKEND_URL/api/ | grep -q "200"; then
  echo "✅ Backend: OK"
else
  echo "❌ Backend: ERREUR"
fi

# Frontend
if curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL | grep -q "200"; then
  echo "✅ Frontend: OK"
else
  echo "❌ Frontend: ERREUR"
fi
```

### Script de Logs

```bash
#!/bin/bash
# get-logs.sh

SERVICE=$1
LIMIT=${2:-100}

if [ -z "$SERVICE" ]; then
  echo "Usage: ./get-logs.sh <service-name> [limit]"
  echo "Example: ./get-logs.sh chatagentb-backend 50"
  exit 1
fi

gcloud run logs read \
  --service $SERVICE \
  --region europe-west1 \
  --limit $LIMIT \
  --format "table(timestamp,severity,textPayload)"
```

## 🆘 Commandes de Dépannage d'Urgence

```bash
# Rollback immédiat vers la version précédente
gcloud run revisions list --service chatagentb-backend --region europe-west1 --limit 2
PREVIOUS_REVISION=$(gcloud run revisions list --service chatagentb-backend --region europe-west1 --format="value(name)" --limit 2 | tail -n 1)
gcloud run services update-traffic chatagentb-backend --to-revisions $PREVIOUS_REVISION=100 --region europe-west1

# Augmenter les ressources d'urgence (trafic élevé)
gcloud run services update chatagentb-backend \
  --memory 8Gi \
  --cpu 4 \
  --max-instances 50 \
  --region europe-west1

# Redémarrer un service (force new deployment)
gcloud run services update chatagentb-backend \
  --region europe-west1 \
  --no-traffic

# Activer le logging détaillé
gcloud logging write test-log "Test message" --severity=INFO
```

---

**💡 Astuce** : Ajoutez ces commandes à vos alias bash/zsh pour un accès rapide !

```bash
# Dans votre ~/.bashrc ou ~/.zshrc
alias gcp-logs='gcloud run logs tail --service chatagentb-backend --region europe-west1'
alias gcp-deploy='gcloud builds submit --config=cloudbuild.yaml'
alias gcp-status='gcloud run services list --region europe-west1'
```

---

**Documentation complète** : [DEPLOY_GCP.md](./DEPLOY_GCP.md)  
**Démarrage rapide** : [QUICKSTART_GCP.md](./QUICKSTART_GCP.md)
