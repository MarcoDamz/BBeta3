# Fonctionnalité : Organisation des Conversations par Dossiers

## 📋 Vue d'ensemble

Cette fonctionnalité permet aux utilisateurs d'organiser leurs conversations dans des dossiers personnalisés. Les dossiers supportent une structure arborescente (dossiers et sous-dossiers) et les conversations peuvent être déplacées par glisser-déposer.

## 🎯 Fonctionnalités implémentées

### Backend (Django)

#### 1. **Modèle `Folder`** (`backend/chat/models.py`)
- **Champs** :
  - `name` : Nom du dossier
  - `user` : Utilisateur propriétaire
  - `parent` : Dossier parent (pour l'arborescence)
  - `order` : Ordre d'affichage
  - `created_at` / `updated_at` : Timestamps

- **Contraintes** :
  - `unique_together` : Un utilisateur ne peut pas avoir deux dossiers avec le même nom au même niveau

#### 2. **Modèle `Conversation` mis à jour**
- Ajout du champ `folder` (ForeignKey vers `Folder`, nullable)
- Permet de classer les conversations dans des dossiers

#### 3. **API REST complète** (`backend/chat/views.py`)

**FolderViewSet** :
- `GET /api/chat/folders/` - Liste des dossiers racine de l'utilisateur
- `POST /api/chat/folders/` - Créer un nouveau dossier
- `GET /api/chat/folders/{id}/` - Détails d'un dossier
- `PATCH /api/chat/folders/{id}/` - Modifier un dossier
- `DELETE /api/chat/folders/{id}/` - Supprimer un dossier
- `POST /api/chat/folders/reorder/` - Réorganiser les dossiers

**ConversationViewSet** (nouvelle action) :
- `POST /api/chat/conversations/{id}/move_to_folder/` - Déplacer une conversation dans un dossier

#### 4. **Serializers** (`backend/chat/serializers.py`)
- `FolderSerializer` : Sérialisation complète avec sous-dossiers et comptage
- `ConversationListSerializer` : Ajout des champs `folder` et `folder_name`

#### 5. **Admin Django** (`backend/chat/admin.py`)
- `FolderAdmin` : Gestion des dossiers dans l'interface admin
- `ConversationAdmin` : Ajout du filtre par dossier

### Frontend (React)

#### 1. **Composant `FolderTree`** (`frontend/src/components/FolderTree.jsx`)
- Affichage arborescent des dossiers
- Expand/Collapse des dossiers
- Drag & Drop des conversations
- Menu contextuel (renommer, supprimer)
- Compteur de conversations par dossier

#### 2. **Composant `Sidebar` mis à jour** (`frontend/src/components/Sidebar.jsx`)
- Bouton "Nouveau dossier"
- Affichage de l'arborescence des dossiers
- Section "Non classées" pour les conversations sans dossier
- Drag & Drop vers la racine pour déclasser une conversation

#### 3. **Store Zustand** (`frontend/src/store/useStore.js`)
- État global pour les dossiers
- Actions :
  - `setFolders` : Charger les dossiers
  - `addFolder` : Ajouter un dossier
  - `updateFolder` : Mettre à jour un dossier
  - `deleteFolder` : Supprimer un dossier
  - `moveConversationToFolder` : Déplacer une conversation

#### 4. **Service API** (`frontend/src/services/api.js`)
```javascript
foldersAPI = {
  list: () => api.get("/chat/folders/"),
  create: (data) => api.post("/chat/folders/", data),
  update: (id, data) => api.patch(`/chat/folders/${id}/`, data),
  delete: (id) => api.delete(`/chat/folders/${id}/`),
  reorder: (folders) => api.post("/chat/folders/reorder/", { folders }),
}

conversationsAPI = {
  ...
  moveToFolder: (id, folderId) => api.post(`/chat/conversations/${id}/move_to_folder/`, { folder_id: folderId }),
}
```

#### 5. **Page Chat** (`frontend/src/pages/ChatPage.jsx`)
- Chargement des dossiers au montage
- Handlers pour :
  - `handleCreateFolder` : Créer un dossier
  - `handleDeleteFolder` : Supprimer un dossier
  - `handleRenameFolder` : Renommer un dossier
  - `handleMoveConversation` : Déplacer une conversation

## 🎨 UX/UI

### Drag & Drop
- **Déplacer une conversation** : Glisser depuis n'importe où et déposer dans un dossier
- **Déclasser une conversation** : Glisser et déposer dans la zone "Non classées"
- **Feedback visuel** : Highlight des zones de dépôt pendant le drag

### Menu contextuel
- Clic sur l'icône ⋮ d'un dossier pour :
  - Renommer le dossier
  - Supprimer le dossier (les conversations ne sont pas supprimées)

### Arborescence
- Icônes `Folder` / `FolderOpen` pour les dossiers
- Icônes `ChevronRight` / `ChevronDown` pour expand/collapse
- Compteur de conversations par dossier

## 📊 Base de données

### Migrations

**Migration `chat/0002_folder_conversation_folder.py`** :
```python
# Créer le modèle Folder
# Ajouter le champ folder à Conversation
```

**État des migrations** :
```bash
chat
 [X] 0001_initial
 [X] 0002_folder_conversation_folder
```

### Schéma

```
┌─────────────────┐
│     Folder      │
├─────────────────┤
│ id              │
│ name            │
│ user_id (FK)    │
│ parent_id (FK)  │──┐ Auto-référence
│ order           │  │ pour l'arborescence
│ created_at      │  │
│ updated_at      │  │
└─────────────────┘  │
         ▲           │
         │           │
         └───────────┘
         │
         │
┌─────────────────┐
│  Conversation   │
├─────────────────┤
│ id              │
│ title           │
│ user_id (FK)    │
│ folder_id (FK)  │──→ Référence vers Folder
│ ...             │
└─────────────────┘
```

## 🔧 Configuration

Aucune configuration supplémentaire n'est nécessaire. La fonctionnalité est automatiquement disponible après :

1. **Migrations appliquées** : `python manage.py migrate`
2. **Services démarrés** : `docker-compose up`

## 🚀 Utilisation

### Créer un dossier
1. Cliquer sur le bouton "Nouveau dossier" dans la sidebar
2. Entrer le nom du dossier
3. Appuyer sur Enter ou cliquer sur "OK"

### Déplacer une conversation
1. Cliquer sur une conversation et maintenir le bouton enfoncé
2. Glisser vers un dossier
3. Relâcher pour déposer

### Gérer un dossier
1. Survoler un dossier
2. Cliquer sur l'icône ⋮ (menu)
3. Choisir "Renommer" ou "Supprimer"

### Déclasser une conversation
1. Glisser une conversation depuis un dossier
2. Déposer dans la zone "Non classées"

## 📝 Notes techniques

### Gestion des permissions
- Les dossiers sont liés à l'utilisateur qui les crée
- Un utilisateur ne peut voir que ses propres dossiers
- Les conversations ne peuvent être déplacées que dans les dossiers de l'utilisateur

### Performances
- Chargement optimisé avec `prefetch_related` pour les sous-dossiers
- Compteur de conversations via annotation SQL
- Pas de rechargement complet lors du drag & drop

### Sécurité
- Validation côté serveur pour s'assurer que :
  - Le dossier appartient à l'utilisateur
  - La conversation appartient à l'utilisateur
  - Les noms de dossiers sont uniques par niveau

## 🐛 Limitations connues

1. **Profondeur de l'arborescence** : Actuellement illimitée (pourrait être restreinte si nécessaire)
2. **Pas de déplacement de dossiers** : Les dossiers ne peuvent pas être déplacés par drag & drop (à implémenter si nécessaire)
3. **Suppression en cascade** : La suppression d'un dossier ne supprime pas les conversations (elles sont déclassées)

## 🔮 Améliorations futures possibles

- [ ] Déplacement de dossiers par drag & drop
- [ ] Limitation de la profondeur de l'arborescence
- [ ] Icônes personnalisées pour les dossiers
- [ ] Tri automatique des conversations dans les dossiers
- [ ] Recherche dans les dossiers
- [ ] Export/Import de la structure de dossiers
- [ ] Partage de dossiers entre utilisateurs
- [ ] Couleurs personnalisées pour les dossiers

## ✅ Tests recommandés

1. **Création de dossier** : Vérifier que le dossier apparaît dans la sidebar
2. **Drag & Drop** : Déplacer une conversation dans un dossier
3. **Renommage** : Renommer un dossier et vérifier la persistence
4. **Suppression** : Supprimer un dossier et vérifier que les conversations sont préservées
5. **Dossiers imbriqués** : Créer un sous-dossier (via l'API ou l'admin)
6. **Permissions** : Vérifier qu'un utilisateur ne peut pas accéder aux dossiers d'un autre

## 📚 Ressources

- **Documentation Django** : https://docs.djangoproject.com/en/5.0/
- **Documentation DRF** : https://www.django-rest-framework.org/
- **Documentation React DnD** : https://github.com/react-dnd/react-dnd (si migration vers une lib)
- **Lucide Icons** : https://lucide.dev/ (icônes utilisées)

---

**Date d'implémentation** : Février 2026  
**Version** : 1.0  
**Statut** : ✅ Implémenté et fonctionnel
