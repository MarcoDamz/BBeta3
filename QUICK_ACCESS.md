# 🚀 Accès Rapide - ChatAgentB v1.1.0

## 🌐 URLs d'accès

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Frontend** | http://localhost:3000 | Interface utilisateur React |
| 🔧 **API Backend** | http://localhost:8000/api/ | API REST (DRF) |
| 👨‍💼 **Admin Django** | http://localhost:8000/admin/ | Interface d'administration |
| 📊 **API Docs** | http://localhost:8000/api/docs/ | Documentation API (si configurée) |

## 🔐 Identifiants par défaut

**Admin Django** :
- **Username** : `admin`
- **Password** : `admin123`

## 📋 Endpoints API principaux

### 🗂️ Dossiers (NOUVEAU v1.1.0)
```bash
GET    http://localhost:8000/api/chat/folders/          # Liste des dossiers
POST   http://localhost:8000/api/chat/folders/          # Créer un dossier
GET    http://localhost:8000/api/chat/folders/{id}/     # Détails d'un dossier
PATCH  http://localhost:8000/api/chat/folders/{id}/     # Modifier un dossier
DELETE http://localhost:8000/api/chat/folders/{id}/     # Supprimer un dossier
POST   http://localhost:8000/api/chat/folders/reorder/  # Réorganiser
```

### 💬 Conversations
```bash
GET    http://localhost:8000/api/chat/conversations/                    # Liste
GET    http://localhost:8000/api/chat/conversations/{id}/               # Détails
POST   http://localhost:8000/api/chat/conversations/                    # Créer
DELETE http://localhost:8000/api/chat/conversations/{id}/               # Supprimer
POST   http://localhost:8000/api/chat/conversations/send_message/       # Envoyer message
POST   http://localhost:8000/api/chat/conversations/{id}/move_to_folder/ # Déplacer (NOUVEAU)
POST   http://localhost:8000/api/chat/conversations/auto_chat/          # Auto-chat
```

### 🤖 Agents
```bash
GET    http://localhost:8000/api/agents/              # Liste
GET    http://localhost:8000/api/agents/{id}/         # Détails
POST   http://localhost:8000/api/agents/              # Créer (admin)
PUT    http://localhost:8000/api/agents/{id}/         # Modifier (admin)
DELETE http://localhost:8000/api/agents/{id}/         # Supprimer (admin)
POST   http://localhost:8000/api/agents/{id}/duplicate/ # Dupliquer (admin)
```

## 🐳 Commandes Docker

### Démarrer
```powershell
docker-compose up -d              # Démarrer en arrière-plan
docker-compose up                 # Démarrer avec logs
```

### Arrêter
```powershell
docker-compose down               # Arrêter tous les services
docker-compose down -v            # Arrêter + supprimer volumes
```

### Redémarrer
```powershell
docker-compose restart            # Tous les services
docker-compose restart backend    # Backend uniquement
docker-compose restart frontend   # Frontend uniquement
```

### Logs
```powershell
docker-compose logs -f            # Tous les logs en temps réel
docker-compose logs -f backend    # Backend uniquement
docker-compose logs -f frontend   # Frontend uniquement
docker-compose logs --tail=50     # 50 dernières lignes
```

### État
```powershell
docker-compose ps                 # Voir l'état des services
docker-compose top                # Voir les processus
```

## 🔧 Commandes Django

### Migrations
```powershell
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py showmigrations
```

### Shell
```powershell
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py dbshell
```

### Créer un superuser
```powershell
docker-compose exec backend python manage.py createsuperuser
```

### Collecter les static files
```powershell
docker-compose exec backend python manage.py collectstatic --noinput
```

## 🧪 Tests rapides

### Test du backend
```powershell
# Liste des agents
curl http://localhost:8000/api/agents/

# Liste des dossiers
curl http://localhost:8000/api/chat/folders/

# Liste des conversations
curl http://localhost:8000/api/chat/conversations/
```

### Test du frontend
1. Ouvrir http://localhost:3000
2. Créer un dossier
3. Créer une conversation
4. Glisser la conversation dans le dossier

## 📊 Monitoring

### Voir les ressources
```powershell
docker stats                      # Utilisation CPU/RAM en temps réel
```

### Inspecter un conteneur
```powershell
docker-compose exec backend sh    # Shell dans le backend
docker-compose exec frontend sh   # Shell dans le frontend
docker-compose exec db psql -U postgres -d chatagentb  # PostgreSQL
docker-compose exec redis redis-cli  # Redis CLI
```

## 🔍 Debugging

### Backend n'est pas accessible ?
```powershell
docker-compose logs backend | Select-String -Pattern "error"
docker-compose restart backend
```

### Frontend n'est pas accessible ?
```powershell
docker-compose logs frontend | Select-String -Pattern "error"
docker-compose restart frontend
```

### Base de données ?
```powershell
docker-compose exec db psql -U postgres -d chatagentb -c "\dt"
```

### Redis ?
```powershell
docker-compose exec redis redis-cli ping
# Doit retourner: PONG
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Documentation principale |
| [QUICKSTART.md](QUICKSTART.md) | Guide de démarrage rapide |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions |
| [IMPLEMENTATION_SUCCESS.md](IMPLEMENTATION_SUCCESS.md) | Résumé de l'implémentation |
| [docs/features/FOLDERS_QUICKSTART.md](docs/features/FOLDERS_QUICKSTART.md) | Guide des dossiers |
| [docs/features/FOLDERS_FEATURE.md](docs/features/FOLDERS_FEATURE.md) | Documentation technique dossiers |
| [docs/api/API.md](docs/api/API.md) | Documentation API complète |

## 🎯 Raccourcis VS Code (si configuré)

| Raccourci | Action |
|-----------|--------|
| `Ctrl+Shift+P` → "Tasks: Run Task" | Exécuter une tâche |
| `Ctrl+Shift+B` | Build (docker-compose up) |

## 💡 Astuces

### Nettoyer complètement
```powershell
docker-compose down -v            # Arrêter + supprimer volumes
docker system prune -a            # Nettoyer Docker (attention!)
```

### Rebuild complet
```powershell
docker-compose build --no-cache
docker-compose up -d
```

### Voir les ports utilisés
```powershell
netstat -ano | findstr ":3000"    # Frontend
netstat -ano | findstr ":8000"    # Backend
netstat -ano | findstr ":5432"    # PostgreSQL
netstat -ano | findstr ":6379"    # Redis
```

## ⚡ Performance

### Vérifier l'utilisation des ressources
```powershell
docker stats --no-stream
```

### Optimiser
```powershell
# Limiter la RAM par service (dans docker-compose.yml)
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
```

## 🆘 Support

En cas de problème :
1. Vérifier les logs : `docker-compose logs -f`
2. Redémarrer les services : `docker-compose restart`
3. Consulter la documentation : `docs/`
4. Vérifier l'état : `docker-compose ps`

## ✅ Checklist de vérification

Avant de commencer à utiliser l'application :

- [ ] Services démarrés : `docker-compose ps`
- [ ] Backend accessible : http://localhost:8000/api/
- [ ] Frontend accessible : http://localhost:3000
- [ ] Admin accessible : http://localhost:8000/admin/
- [ ] Migrations appliquées : `docker-compose exec backend python manage.py showmigrations`
- [ ] Clés API configurées dans `.env`
- [ ] Au moins un agent créé dans l'admin

## 🎉 Tout est prêt !

L'application ChatAgentB v1.1.0 avec le système de dossiers est opérationnelle !

**Profitez de votre nouvelle fonctionnalité d'organisation ! 🗂️**

---

**Version** : 1.1.0  
**Date** : 7 février 2026  
**Status** : ✅ OPÉRATIONNEL
