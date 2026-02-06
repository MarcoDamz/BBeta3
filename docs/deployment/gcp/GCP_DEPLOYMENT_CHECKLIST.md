# ✅ Checklist de Pré-Déploiement GCP

Avant de déployer ChatAgentB sur Google Cloud Platform, vérifiez que tous ces éléments sont en place.

## 📋 Prérequis (à faire une seule fois)

### 1. Compte et Projet GCP
- [ ] Compte Google Cloud Platform créé
- [ ] Projet GCP créé (ex: `mon-chatagentb-project`)
- [ ] Facturation activée sur le projet
- [ ] Quota suffisant pour :
  - Cloud Run (3 services minimum)
  - Cloud SQL (1 instance PostgreSQL)
  - Memorystore Redis (1 instance)

### 2. Outils Installés
- [ ] **Google Cloud SDK** installé et configuré
  - Windows : [Télécharger ici](https://cloud.google.com/sdk/docs/install)
  - Mac : `brew install --cask google-cloud-sdk`
  - Linux : `curl https://sdk.cloud.google.com | bash`
- [ ] **gcloud** CLI accessible dans le terminal
  - Test : `gcloud --version`
- [ ] **Docker** installé (pour tests locaux optionnels)

### 3. Authentification GCP
- [ ] Authentifié avec `gcloud auth login`
- [ ] Projet par défaut configuré : `gcloud config set project VOTRE_PROJECT_ID`
- [ ] Vérification : `gcloud config get-value project`

## 🔐 Secrets et Configuration

### 4. Clés API et Secrets
- [ ] Clé API OpenAI obtenue (ou Azure OpenAI, Anthropic)
  - Format : `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- [ ] Mot de passe sécurisé pour la base de données défini
  - Minimum 12 caractères, alphanumérique + symboles
- [ ] Mot de passe admin Django défini (pour le superuser)
- [ ] Secret key Django générée (50 caractères aléatoires)
  - Ou laisser le script la générer automatiquement

### 5. Configuration du Code
- [ ] Fichier `.env.example` vérifié
- [ ] Variables d'environnement sensibles **JAMAIS** committées dans Git
- [ ] `.gitignore` inclut `.env` et fichiers sensibles

## 🏗️ Fichiers de Déploiement

### 6. Fichiers Docker
- [ ] `backend/Dockerfile.cloudrun` existe
- [ ] `backend/Dockerfile.worker` existe
- [ ] `frontend/Dockerfile.cloudrun` existe
- [ ] `backend/docker-entrypoint-cloudrun.sh` est exécutable
- [ ] `frontend/docker-entrypoint-cloudrun.sh` est exécutable

### 7. Configuration Cloud Build
- [ ] `cloudbuild.yaml` existe à la racine
- [ ] Substitutions configurées :
  - `_REGION` (ex: europe-west1)
  - `_CLOUDSQL_INSTANCE`
  - `_DB_NAME`
  - `_DB_USER`
  - `_REDIS_HOST`

### 8. Scripts de Déploiement
- [ ] `deploy-gcp.ps1` (Windows) ou `deploy-gcp.sh` (Linux/Mac) existe
- [ ] Script est exécutable : `chmod +x deploy-gcp.sh` (Linux/Mac)

## 🌐 Réseau et Domaine (Optionnel)

### 9. Configuration Domaine Personnalisé
- [ ] Nom de domaine acheté (si nécessaire)
- [ ] DNS configuré pour pointer vers Cloud Run
- [ ] Certificat SSL/TLS configuré (Cloud Run gère automatiquement)

### 10. CORS et Sécurité
- [ ] `ALLOWED_HOSTS` configuré dans `settings.py`
- [ ] `CORS_ALLOWED_ORIGINS` configuré
- [ ] `CSRF_TRUSTED_ORIGINS` configuré

## 🧪 Tests Pré-Déploiement

### 11. Tests Locaux (Recommandés)
- [ ] Application testée localement avec Docker Compose
  - `docker-compose up --build`
- [ ] Tests des endpoints API :
  - `curl http://localhost:8000/api/agents/`
- [ ] Interface frontend accessible :
  - `http://localhost:3000`
- [ ] Admin Django accessible et fonctionnel :
  - `http://localhost:8000/admin/`
- [ ] Tâches Celery fonctionnent (génération de titres, auto-chat)

### 12. Vérification du Code
- [ ] Pas d'erreurs dans les logs backend : `docker-compose logs backend`
- [ ] Pas d'erreurs dans les logs frontend : `docker-compose logs frontend`
- [ ] Migrations Django appliquées : `docker-compose exec backend python manage.py migrate`

## 💰 Budget et Coûts

### 13. Estimation des Coûts
- [ ] Budget mensuel estimé : ~$100-120/mois (config minimale)
- [ ] Budget GCP configuré avec alertes :
  ```bash
  gcloud billing budgets create \
    --billing-account=BILLING_ACCOUNT_ID \
    --display-name="ChatAgentB Budget" \
    --budget-amount=150USD
  ```
- [ ] Alertes configurées à 50%, 80%, 100% du budget

### 14. Optimisations Prévues
- [ ] Autoscaling à 0 instance min (économie mais cold start)
- [ ] Tiers gratuits activés (Cloud Run offre 2M requêtes/mois)
- [ ] Instances réduites en période creuse

## 📊 Monitoring et Observabilité

### 15. Logging et Monitoring
- [ ] Cloud Logging activé (par défaut avec Cloud Run)
- [ ] Cloud Monitoring configuré (dashboards personnalisés optionnels)
- [ ] Alertes d'erreur configurées :
  ```bash
  # Alerte si taux d'erreur > 5%
  gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="ChatAgentB Error Rate" \
    --condition-display-name="Error rate > 5%" \
    --condition-threshold-value=5
  ```

## 🚀 Déploiement

### 16. Lancement du Déploiement
- [ ] Tous les prérequis ci-dessus validés ✅
- [ ] Commande de déploiement prête :
  ```powershell
  # Windows
  .\deploy-gcp.ps1 -ProjectId "mon-chatagentb-project" -Region "europe-west1"
  
  # Linux/Mac
  ./deploy-gcp.sh mon-chatagentb-project europe-west1
  ```
- [ ] Temps estimé : 15-20 minutes pour le déploiement initial

### 17. Post-Déploiement
- [ ] URLs des services notées :
  - Backend : `https://chatagentb-backend-xxx.run.app`
  - Frontend : `https://chatagentb-frontend-xxx.run.app`
  - Admin : `https://chatagentb-backend-xxx.run.app/admin/`
- [ ] Superuser créé via variables d'environnement ou commande
- [ ] Tests des endpoints en production :
  ```bash
  curl https://chatagentb-backend-xxx.run.app/api/agents/
  ```
- [ ] Interface accessible depuis un navigateur
- [ ] Logs vérifiés : `gcloud run logs read --service chatagentb-backend`

## 🔄 CI/CD (Optionnel mais Recommandé)

### 18. Intégration Continue
- [ ] Dépôt GitHub/GitLab configuré
- [ ] Trigger Cloud Build créé :
  ```bash
  gcloud builds triggers create github \
    --repo-name=chatagentb \
    --repo-owner=votre-username \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml
  ```
- [ ] Push sur `main` déclenche automatiquement le déploiement

## 📚 Documentation

### 19. Documentation Lue
- [ ] [QUICKSTART_GCP.md](./QUICKSTART_GCP.md) - Démarrage rapide
- [ ] [DEPLOY_GCP.md](./DEPLOY_GCP.md) - Documentation complète
- [ ] [GCP_DEPLOYMENT_SUMMARY.md](./GCP_DEPLOYMENT_SUMMARY.md) - Résumé des commandes

### 20. Support et Aide
- [ ] Accès à la [documentation officielle GCP](https://cloud.google.com/docs)
- [ ] Contact support prévu en cas de problème
- [ ] Canal de communication configuré (Slack, email, etc.)

---

## ✅ Validation Finale

**Tous les items ci-dessus sont cochés ?** 🎉

Vous êtes prêt à déployer ChatAgentB sur GCP !

```powershell
# Windows
.\deploy-gcp.ps1 -ProjectId "mon-chatagentb-project" -Region "europe-west1"

# Linux/Mac
./deploy-gcp.sh mon-chatagentb-project europe-west1
```

**Bon déploiement !** 🚀

---

## 🆘 En cas de problème

1. **Consulter les logs** :
   ```bash
   gcloud run logs read --service chatagentb-backend --limit=100
   ```

2. **Vérifier la configuration** :
   ```bash
   gcloud run services describe chatagentb-backend --format=yaml
   ```

3. **Rollback si nécessaire** :
   ```bash
   gcloud run revisions list --service chatagentb-backend
   gcloud run services update-traffic chatagentb-backend \
     --to-revisions=PREVIOUS_REVISION=100
   ```

4. **Contacter le support** : Voir [DEPLOY_GCP.md](./DEPLOY_GCP.md) section Troubleshooting
