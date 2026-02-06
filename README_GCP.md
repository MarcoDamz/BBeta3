# 🚀 Déployer ChatAgentB sur Google Cloud Platform

## 🎯 Par Où Commencer ?

### Vous voulez déployer RAPIDEMENT ?
👉 **[START_HERE_GCP.md](./START_HERE_GCP.md)** ⭐

### Vous voulez une vue d'ensemble visuelle ?
👉 **[GCP_VISUAL_GUIDE.md](./GCP_VISUAL_GUIDE.md)** 🎨

### Vous voulez un guide pas-à-pas détaillé ?
👉 **[QUICKSTART_GCP.md](./QUICKSTART_GCP.md)** 📘

### Vous cherchez la documentation complète ?
👉 **[DEPLOY_GCP.md](./DEPLOY_GCP.md)** 📚

### Vous cherchez une information spécifique ?
👉 **[GCP_DOCUMENTATION_INDEX.md](./GCP_DOCUMENTATION_INDEX.md)** 🗺️

---

## ⚡ Déploiement en 1 Commande

### Windows (PowerShell)
```powershell
.\deploy-gcp.ps1 -ProjectId "votre-projet-gcp" -Region "europe-west1"
```

### Linux/Mac (Bash)
```bash
./deploy-gcp.sh votre-projet-gcp europe-west1
```

**C'est tout !** Le script gère tout automatiquement. ⏱️ **15-20 minutes**

---

## 📋 Prérequis (5 minutes)

1. **Installer gcloud CLI** : https://cloud.google.com/sdk/docs/install
2. **S'authentifier** : `gcloud auth login`
3. **Configurer le projet** : `gcloud config set project VOTRE_PROJECT_ID`
4. **Avoir sa clé API OpenAI** (ou Azure OpenAI, Anthropic)

---

## ✅ Vérifier Avant de Déployer

```powershell
# Windows
.\check-gcp-ready.ps1

# Linux/Mac
./check-gcp-ready.sh
```

Ce script vérifie automatiquement tous les prérequis.

---

## 📚 Toute la Documentation

| Fichier | Description | Pour Qui ? |
|---------|-------------|------------|
| **[START_HERE_GCP.md](./START_HERE_GCP.md)** | Point d'entrée principal | 🌟 Tous |
| **[GCP_VISUAL_GUIDE.md](./GCP_VISUAL_GUIDE.md)** | Guide visuel ASCII | 🎨 Débutants |
| **[QUICKSTART_GCP.md](./QUICKSTART_GCP.md)** | Démarrage rapide (5 min) | ⚡ Pressés |
| **[DEPLOY_GCP.md](./DEPLOY_GCP.md)** | Documentation exhaustive | 📚 Experts |
| **[GCP_DEPLOYMENT_CHECKLIST.md](./GCP_DEPLOYMENT_CHECKLIST.md)** | Checklist prérequis | ✅ Méthodiques |
| **[GCP_DEPLOYMENT_SUMMARY.md](./GCP_DEPLOYMENT_SUMMARY.md)** | Résumé technique | 🔧 DevOps |
| **[GCP_COMMANDS.md](./GCP_COMMANDS.md)** | Référence commandes | 🛠️ Admin Sys |
| **[GCP_DOCUMENTATION_INDEX.md](./GCP_DOCUMENTATION_INDEX.md)** | Index complet | 🗺️ Navigateurs |
| **[GCP_SETUP_COMPLETE.md](./GCP_SETUP_COMPLETE.md)** | Résumé config | 📊 PM/Tech Leads |

---

## 🏗️ Architecture

```
Google Cloud Platform
├── Cloud Run (Frontend)    → React + Nginx
├── Cloud Run (Backend)     → Django + DRF
├── Cloud Run (Worker)      → Celery
├── Cloud SQL               → PostgreSQL 15
├── Memorystore             → Redis 7
└── Secret Manager          → Secrets sécurisés
```

---

## 💰 Coûts : ~$103-122/mois

- Cloud Run : ~$58-77/mois (3 services)
- Cloud SQL : ~$10/mois
- Redis : ~$35/mois

💡 **Cloud Run offre 2M requêtes gratuites/mois**

---

## 🎯 Prochaine Étape

1. **Lire** : [START_HERE_GCP.md](./START_HERE_GCP.md)
2. **Vérifier** : `.\check-gcp-ready.ps1`
3. **Déployer** : `.\deploy-gcp.ps1 -ProjectId "votre-projet"`

---

## 🆘 Besoin d'Aide ?

- **Troubleshooting** : [DEPLOY_GCP.md - Section Troubleshooting](./DEPLOY_GCP.md)
- **Commandes utiles** : [GCP_COMMANDS.md](./GCP_COMMANDS.md)
- **Index complet** : [GCP_DOCUMENTATION_INDEX.md](./GCP_DOCUMENTATION_INDEX.md)

---

**Bon déploiement !** 🚀🌐✨
