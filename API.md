# 📡 Documentation API - ChatAgentB

## Base URL
```
http://localhost:8000/api
```

## Authentication
L'API utilise l'authentification par session Django (cookies).

Pour les requêtes AJAX depuis le frontend, le cookie CSRF est automatiquement géré.

---

## 🤖 Agents

### Liste des agents
```http
GET /api/agents/
```

**Réponse** (200 OK) :
```json
[
  {
    "id": 1,
    "name": "Assistant Python",
    "description": "Expert en programmation Python",
    "categories": ["développement", "python"],
    "llm_model": "azure.gpt-4.1",
    "is_active": true
  }
]
```

### Détails d'un agent
```http
GET /api/agents/{id}/
```

**Réponse** (200 OK) :
```json
{
  "id": 1,
  "name": "Assistant Python",
  "description": "Expert en programmation Python",
  "categories": ["développement", "python"],
  "llm_model": "azure.gpt-4.1",
  "system_prompt": "Tu es un expert en Python...",
  "temperature": 0.7,
  "max_tokens": 2000,
  "is_active": true,
  "created_at": "2024-01-25T10:00:00Z",
  "updated_at": "2024-01-25T10:00:00Z"
}
```

### Créer un agent (Admin uniquement)
```http
POST /api/agents/
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "name": "Nouvel Agent",
  "description": "Description de l'agent",
  "categories": ["tag1", "tag2"],
  "llm_model": "azure.gpt-4.1",
  "system_prompt": "Tu es un assistant...",
  "temperature": 0.7,
  "max_tokens": 2000,
  "is_active": true
}
```

**Réponse** (201 Created) :
```json
{
  "id": 5,
  "name": "Nouvel Agent",
  ...
}
```

### Modifier un agent (Admin uniquement)
```http
PUT /api/agents/{id}/
Content-Type: application/json
```

**Corps de la requête** : (même structure que POST)

**Réponse** (200 OK) : Agent modifié

### Supprimer un agent (Admin uniquement)
```http
DELETE /api/agents/{id}/
```

**Réponse** (204 No Content)

### Dupliquer un agent (Admin uniquement)
```http
POST /api/agents/{id}/duplicate/
```

**Réponse** (201 Created) :
```json
{
  "id": 6,
  "name": "Assistant Python (Copie)",
  "is_active": false,
  ...
}
```

---

## 💬 Conversations

### Liste des conversations
```http
GET /api/chat/conversations/
```

**Réponse** (200 OK) :
```json
[
  {
    "id": 1,
    "title": "Discussion sur Python",
    "conversation_type": "user",
    "agents_details": [
      {
        "id": 1,
        "name": "Assistant Python",
        "llm_model": "azure.gpt-4.1"
      }
    ],
    "message_count": 10,
    "last_message": {
      "content": "D'accord, je comprends...",
      "role": "ai",
      "created_at": "2024-01-25T14:30:00Z"
    },
    "created_at": "2024-01-25T10:00:00Z",
    "updated_at": "2024-01-25T14:30:00Z"
  }
]
```

### Détails d'une conversation
```http
GET /api/chat/conversations/{id}/
```

**Réponse** (200 OK) :
```json
{
  "id": 1,
  "title": "Discussion sur Python",
  "conversation_type": "user",
  "user": 1,
  "agents": [1],
  "agents_details": [...],
  "messages": [
    {
      "id": 1,
      "role": "human",
      "content": "Bonjour !",
      "agent": null,
      "agent_name": null,
      "is_auto_chat": false,
      "metadata": {},
      "created_at": "2024-01-25T10:00:00Z"
    },
    {
      "id": 2,
      "role": "ai",
      "content": "Bonjour ! Comment puis-je vous aider ?",
      "agent": 1,
      "agent_name": "Assistant Python",
      "is_auto_chat": false,
      "metadata": {},
      "created_at": "2024-01-25T10:00:05Z"
    }
  ],
  "message_count": 2,
  "created_at": "2024-01-25T10:00:00Z",
  "updated_at": "2024-01-25T10:00:05Z"
}
```

### Créer une conversation
```http
POST /api/chat/conversations/
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "agents": [1]
}
```

**Réponse** (201 Created) : Conversation créée

### Supprimer une conversation
```http
DELETE /api/chat/conversations/{id}/
```

**Réponse** (204 No Content)

### Envoyer un message
```http
POST /api/chat/conversations/send_message/
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "message": "Comment créer une API REST avec Django ?",
  "agent_id": 1,
  "conversation_id": 1  // Optionnel, créé automatiquement si absent
}
```

**Réponse** (200 OK) :
```json
{
  "conversation_id": 1,
  "user_message": {
    "id": 3,
    "role": "human",
    "content": "Comment créer une API REST avec Django ?",
    "created_at": "2024-01-25T14:00:00Z"
  },
  "ai_message": {
    "id": 4,
    "role": "ai",
    "content": "Pour créer une API REST avec Django, je recommande...",
    "agent": 1,
    "agent_name": "Assistant Python",
    "created_at": "2024-01-25T14:00:05Z"
  }
}
```

### Lancer un Auto-Chat (Admin uniquement)
```http
POST /api/chat/conversations/auto_chat/
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "agent_a_id": 1,
  "agent_b_id": 2,
  "initial_message": "Discutons des avantages de Python vs JavaScript",
  "iterations": 10
}
```

**Réponse** (202 Accepted) :
```json
{
  "status": "started",
  "task_id": "abc123-def456-...",
  "message": "Auto-chat lancé avec 10 itérations"
}
```

**Note** : La tâche s'exécute en arrière-plan via Celery. Consulter l'historique des conversations pour voir le résultat.

---

## 📨 Messages

### Liste des messages
```http
GET /api/chat/messages/
```

**Réponse** (200 OK) :
```json
[
  {
    "id": 1,
    "conversation": 1,
    "role": "human",
    "content": "Bonjour !",
    "agent": null,
    "agent_name": null,
    "is_auto_chat": false,
    "metadata": {},
    "created_at": "2024-01-25T10:00:00Z"
  }
]
```

### Détails d'un message
```http
GET /api/chat/messages/{id}/
```

**Réponse** (200 OK) : Détails du message

---

## 🔐 Permissions

| Endpoint | Authentifié | Admin |
|----------|-------------|-------|
| GET /api/agents/ | ✅ | - |
| GET /api/agents/{id}/ | ✅ | - |
| POST /api/agents/ | - | ✅ |
| PUT /api/agents/{id}/ | - | ✅ |
| DELETE /api/agents/{id}/ | - | ✅ |
| POST /api/agents/{id}/duplicate/ | - | ✅ |
| GET /api/chat/conversations/ | ✅ | - |
| POST /api/chat/conversations/send_message/ | ✅ | - |
| POST /api/chat/conversations/auto_chat/ | - | ✅ |

---

## ⚠️ Codes d'Erreur

### 400 Bad Request
```json
{
  "error": "Message manquant ou invalide"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "error": "Agent introuvable ou inactif"
}
```

### 500 Internal Server Error
```json
{
  "error": "Erreur lors de la génération de la réponse: ..."
}
```

---

## 🧪 Tests avec cURL

### Obtenir la liste des agents
```bash
curl -X GET http://localhost:8000/api/agents/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Envoyer un message
```bash
curl -X POST http://localhost:8000/api/chat/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "message": "Bonjour !",
    "agent_id": 1
  }'
```

---

## 📚 Ressources Complémentaires

- **Django REST Framework** : https://www.django-rest-framework.org/
- **LangChain** : https://python.langchain.com/
- **Celery** : https://docs.celeryq.dev/

---

Pour toute question, consultez le [README.md](README.md) ou le [QUICKSTART.md](QUICKSTART.md).
