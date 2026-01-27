# 🚀 Guide de Démarrage Rapide - ChatAgentB

## En 5 minutes chrono ! ⏱️

### 1️⃣ Prérequis

- ✅ Docker Desktop installé et démarré
- ✅ Clé API OpenAI

### 2️⃣ Configuration

1. **Éditer le fichier `.env`** à la racine du projet :

```env
# ⚠️ OBLIGATOIRE - Remplacez par votre vraie clé
OPENAI_API_KEY=sk-votre-cle-openai-ici

# OPTIONNEL - URL de base personnalisée (laissez vide par défaut)
OPENAI_API_BASE=
```

### 3️⃣ Démarrage

**Option A : Via PowerShell (Recommandé)**
```powershell
.\start.ps1
```

**Option B : Via Docker Compose**
```powershell
docker-compose up --build -d
```

**Option C : Via VS Code**
- `Ctrl+Shift+P` → "Tasks: Run Task" → "🚀 Démarrer ChatAgentB"

### 4️⃣ Accéder à l'application

- 🌐 **Interface utilisateur** : http://localhost:3000
- 🔧 **Admin Django** : http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`

### 5️⃣ Créer des agents de démo (Optionnel)

```powershell
docker-compose exec backend python create_demo_agents.py
```

Cela crée 6 agents préconfigurés :
- 🐍 Assistant Python
- ⚛️ Expert JavaScript
- ☁️ Architecte Cloud
- 📊 Analyste de Données
- 🎨 Assistant Créatif
- 👨‍🏫 Professeur Pédagogue

---

## 📝 Premier Agent Manuellement

### Via l'Interface Web

1. Ouvrir http://localhost:3000
2. Cliquer sur **"Admin Config"**
3. Cliquer sur **"Nouvel Agent"**
4. Remplir le formulaire :

```
Nom: Mon Premier Agent
Modèle LLM: azure.gpt-4.1
System Prompt: Tu es un assistant utile et amical.
Température: 0.7
Max Tokens: 2000
```

5. Cocher **"Agent actif"**
6. Cliquer sur **"Créer"**

### Via l'Admin Django

1. Ouvrir http://localhost:8000/admin/
2. Se connecter (admin / admin123)
3. Cliquer sur **"Agents"** → **"Ajouter un agent"**
4. Remplir et sauvegarder

---

## 💬 Première Conversation

1. Retour sur http://localhost:3000
2. Sélectionner un agent dans le menu déroulant
3. Taper un message : *"Bonjour ! Peux-tu m'aider ?"*
4. Appuyer sur **"Envoyer"**
5. 🎉 Votre première conversation !

---

## 🤖 Premier Auto-Chat

1. Créer au moins 2 agents différents
2. Page Admin → Bouton **"Mode Auto-Chat"**
3. Configuration :

```
Agent A: Assistant Python
Agent B: Expert JavaScript
Message Initial: Discutons des avantages et inconvénients de Python vs JavaScript pour le développement web.
Itérations: 5
```

4. Cliquer sur **"Lancer"**
5. Consulter le résultat dans l'historique (titre "AUTO: ...")

---

## 🛠️ Commandes Utiles

### Voir les logs en temps réel
```powershell
docker-compose logs -f
```

### Voir les logs d'un service spécifique
```powershell
docker-compose logs -f backend
docker-compose logs -f worker
```

### Arrêter l'application
```powershell
.\stop.ps1
# ou
docker-compose down
```

### Redémarrer après des modifications
```powershell
docker-compose restart backend
docker-compose restart frontend
```

### Accéder au shell Django
```powershell
docker-compose exec backend python manage.py shell
```

---

## ❓ Problèmes Courants

### "LLM API Key not found"
- ✅ Vérifier que les clés sont dans `.env`
- ✅ Redémarrer : `docker-compose restart`

### Le backend ne démarre pas
```powershell
# Voir les logs
docker-compose logs backend

# Réinitialiser la base de données
docker-compose down -v
docker-compose up -d
```

### Le frontend affiche une erreur
```powershell
# Reconstruire l'image
docker-compose up -d --build frontend
```

### Celery ne traite pas les tâches
```powershell
# Vérifier Redis
docker-compose exec redis redis-cli ping
# Réponse attendue: PONG

# Redémarrer le worker
docker-compose restart worker
```

---

## 🎯 Prochaines Étapes

1. ✅ Créer plusieurs agents avec des personnalités différentes
2. ✅ Tester différentes températures (0.0 = déterministe, 1.0 = créatif)
3. ✅ Essayer le mode Auto-Chat avec différents agents
4. ✅ Explorer l'API : http://localhost:8000/api/
5. ✅ Lire le README complet pour les fonctionnalités avancées

---

## 📚 Documentation Complète

Pour plus de détails, consultez le [README.md](README.md) principal.

---

**Amusez-vous bien avec ChatAgentB ! 🚀**
