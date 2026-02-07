# 🚀 Guide de Démarrage Rapide - Système de Dossiers

## ✨ Nouvelle Fonctionnalité : Organisez vos conversations !

Vous pouvez maintenant organiser vos conversations dans des dossiers personnalisés, exactement comme dans un gestionnaire de fichiers.

## 📺 Démonstration en 5 étapes

### 1. Créer un dossier

1. Ouvrez l'application : http://localhost:3000
2. Dans la sidebar à gauche, cliquez sur **"Nouveau dossier"**
3. Entrez un nom (ex: "Projets", "Personnel", "Travail")
4. Appuyez sur **Enter** ou cliquez sur **OK**

### 2. Créer une conversation

1. Cliquez sur **"Nouvelle conversation"**
2. Sélectionnez un agent
3. Commencez à discuter !

### 3. Déplacer une conversation dans un dossier

**Méthode Drag & Drop** :
1. Cliquez sur une conversation et **maintenez le bouton enfoncé**
2. Glissez la conversation vers un dossier
3. Relâchez pour déposer

La conversation apparaît maintenant dans le dossier ! 🎉

### 4. Gérer un dossier

**Menu contextuel** :
1. Survolez un dossier
2. Cliquez sur l'icône **⋮** (trois points)
3. Choisissez :
   - **Renommer** : Modifier le nom du dossier
   - **Supprimer** : Supprimer le dossier (les conversations sont préservées)

### 5. Déclasser une conversation

Pour retirer une conversation d'un dossier :
1. Glissez la conversation depuis le dossier
2. Déposez-la dans la zone **"NON CLASSÉES"** en bas de la sidebar

## 🎯 Cas d'usage

### 📁 Organisation par projet
```
📂 Projet Alpha
  💬 Discussion architecture
  💬 Brainstorming features
  💬 Review code

📂 Projet Beta
  💬 Spécifications
  💬 Questions techniques
```

### 📁 Organisation par agent
```
📂 ChatGPT Conversations
  💬 Aide Python
  💬 Explications Django

📂 Claude Conversations
  💬 Analyse de code
  💬 Documentation
```

### 📁 Organisation par thème
```
📂 Développement Web
  💬 React & Vite
  💬 Django REST
  💬 Déploiement

📂 Machine Learning
  💬 TensorFlow
  💬 LangChain
```

## 💡 Astuces

### ✅ Bonnes pratiques
- **Nommez clairement vos dossiers** : "Projets", "Personnel", "Travail"
- **Créez des sous-dossiers** via l'admin pour une organisation avancée
- **Utilisez le compteur** : Le nombre entre parenthèses indique combien de conversations sont dans le dossier
- **Expand/Collapse** : Cliquez sur la flèche (▶/▼) pour ouvrir/fermer un dossier

### 🎨 Interface
- **Icône 📁** : Dossier fermé
- **Icône 📂** : Dossier ouvert
- **Icône ▶** : Cliquer pour ouvrir
- **Icône ▼** : Cliquer pour fermer
- **Icône ⋮** : Menu contextuel (affiché au survol)

### 🔒 Sécurité
- Chaque utilisateur voit uniquement ses propres dossiers
- Les dossiers sont sauvegardés en base de données
- Les conversations ne sont jamais supprimées avec les dossiers

## 🛠️ Fonctionnalités avancées

### Via l'interface Admin (http://localhost:8000/admin/)

**Créer des sous-dossiers** :
1. Connectez-vous à l'admin (admin / admin123)
2. Allez dans **Chat > Dossiers**
3. Cliquez sur **Ajouter un dossier**
4. Dans le champ **Dossier parent**, sélectionnez un dossier existant
5. Sauvegardez

**Résultat** : Vous avez maintenant une hiérarchie !
```
📂 Projets
  📂 2024
    💬 Projet A
    💬 Projet B
  📂 2025
    💬 Projet C
```

### Réorganiser les dossiers
Les dossiers sont triés par :
1. **Ordre** (champ `order` modifiable via l'admin)
2. **Nom** (alphabétique)

## 🐛 Dépannage

### Le dossier n'apparaît pas ?
- Vérifiez que vous êtes connecté
- Rafraîchissez la page (F5)
- Vérifiez les logs : `docker-compose logs -f backend`

### La conversation ne se déplace pas ?
- Vérifiez que vous glissez bien jusqu'au dossier
- Attendez le changement de couleur (highlight)
- Relâchez le bouton de la souris

### Erreur lors de la création ?
- Vérifiez que le backend est démarré : `docker-compose ps`
- Vérifiez que le nom du dossier n'existe pas déjà

## 📞 Support

En cas de problème :
1. **Logs** : `docker-compose logs -f`
2. **Redémarrer** : `docker-compose restart`
3. **Documentation complète** : `docs/features/FOLDERS_FEATURE.md`

## 🎉 Amusez-vous bien avec votre nouvelle organisation !

L'équipe vous souhaite une excellente expérience avec cette nouvelle fonctionnalité ! 🚀

---

**Version** : 1.0  
**Date** : Février 2026
