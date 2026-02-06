# Frontend - Dockerfiles Expliqués

Ce dossier contient plusieurs Dockerfiles pour différents environnements de déploiement.

## 📁 Fichiers Docker

### 1. `Dockerfile` - Développement Local (Docker Compose)
**Usage** : Environnement de développement local avec hot-reload et Nginx

```bash
docker-compose up --build
```

**Architecture** :
- **Stage 1 (builder)** : Build React avec Vite
- **Stage 2 (production)** : Nginx pour servir les fichiers statiques

**Caractéristiques** :
- ✅ Build multi-stage optimisé
- ✅ Nginx Alpine (léger)
- ✅ Port 80
- ✅ Configuration Nginx pour SPA

### 2. `Dockerfile.cloudrun` - Production GCP Cloud Run
**Usage** : Déploiement du frontend React sur Cloud Run

```bash
gcloud builds submit --config=../cloudbuild.yaml
```

**Architecture** :
- **Stage 1 (builder)** : Build React avec variables d'environnement
- **Stage 2 (production)** : Nginx Alpine avec configuration Cloud Run

**Caractéristiques** :
- ✅ Port 8080 (Cloud Run standard)
- ✅ Configuration Nginx dynamique (envsubst)
- ✅ Health check endpoint (`/health`)
- ✅ Gzip compression
- ✅ Cache des assets statiques
- ✅ Routing SPA (fallback vers index.html)

**Build Args** :
- `VITE_API_URL` : URL du backend (ex: `https://backend-xxx.run.app`)

## 🔧 Configuration Nginx

### `nginx.conf` - Local Development
Configuration Nginx pour Docker Compose :
- Port : 80
- Gestion SPA (React Router)
- Proxy vers backend local (optionnel)

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### `nginx.cloudrun.conf` - Cloud Run Production
Configuration Nginx optimisée pour Cloud Run :
- Port : Dynamique via variable `${PORT}`
- Health check endpoint
- Cache agressif des assets
- Gzip compression
- Security headers

```nginx
server {
    listen ${PORT};
    
    # Cache assets 1 an
    location ~* \.(js|css|png|jpg|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check
    location /health {
        return 200 "healthy\n";
    }
    
    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 🚀 Scripts d'Entrée

### `docker-entrypoint-cloudrun.sh`
Script de démarrage pour Cloud Run :
1. Substitue les variables d'environnement dans la config Nginx
   - `${PORT}` → Port Cloud Run (8080)
2. Lance Nginx en mode foreground

```bash
#!/bin/sh
envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
exec nginx -g 'daemon off;'
```

## 📦 Variables d'Environnement

### Build Time (Vite)

Ces variables sont injectées lors du **build** (compilées dans le code) :

```bash
# URL du backend API
VITE_API_URL=https://chatagentb-backend-xxx.run.app
```

**⚠️ Important** : Les variables `VITE_*` doivent être définies au **build**, pas au runtime.

### Runtime (Nginx)

Ces variables sont utilisées au **démarrage** du container :

```bash
# Port d'écoute (Cloud Run)
PORT=8080  # Automatique sur Cloud Run
```

## 🏗️ Processus de Build

### Local Development

```bash
# Depuis la racine du projet
docker-compose up --build frontend

# Ou rebuild complet
docker-compose build --no-cache frontend
```

### Cloud Run Production

```bash
# Build avec URL backend
cd frontend
gcloud builds submit \
  -t gcr.io/PROJECT_ID/chatagentb-frontend:latest \
  -f Dockerfile.cloudrun \
  --build-arg VITE_API_URL=https://backend-xxx.run.app .

# Déployer
gcloud run deploy chatagentb-frontend \
  --image gcr.io/PROJECT_ID/chatagentb-frontend:latest \
  --region europe-west1 \
  --allow-unauthenticated
```

### Via Cloud Build (Automatique)

Le fichier `cloudbuild.yaml` gère le build automatiquement :

```yaml
- name: 'gcr.io/cloud-builders/docker'
  args:
    - 'build'
    - '--build-arg'
    - 'VITE_API_URL=https://backend-${_REGION}-${PROJECT_ID}.a.run.app'
    - '-t'
    - 'gcr.io/$PROJECT_ID/chatagentb-frontend:latest'
    - '-f'
    - 'Dockerfile.cloudrun'
    - '.'
```

## 🔍 Différences entre les Dockerfiles

| Aspect | Dockerfile (local) | Dockerfile.cloudrun |
|--------|-------------------|---------------------|
| **Port** | 80 | 8080 (Cloud Run) |
| **Config Nginx** | Statique | Dynamique (envsubst) |
| **API URL** | http://localhost:8000 | Build arg (Cloud Run) |
| **Health Check** | ❌ | ✅ `/health` |
| **Cache** | Basique | Agressif (1 an) |
| **Compression** | ✅ Gzip | ✅ Gzip optimisé |
| **Security Headers** | ❌ | ✅ (X-Frame, etc.) |

## 📊 Structure des Fichiers Build

### Après Build Local
```
frontend/dist/
├── index.html
├── assets/
│   ├── index-abc123.js
│   ├── index-def456.css
│   └── logo-ghi789.svg
└── vite.svg
```

### Dans le Container
```
/usr/share/nginx/html/
├── index.html
├── assets/
│   ├── index-abc123.js  (cache: 1 an)
│   ├── index-def456.css  (cache: 1 an)
│   └── logo-ghi789.svg   (cache: 1 an)
└── vite.svg
```

## 🔧 Configuration React/Vite

### `vite.config.js`
Configuration pour le proxy de développement (optionnel) :

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
});
```

### `src/services/api.js`
Configuration de l'URL API :

```javascript
// Utilise la variable d'environnement ou fallback
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const agentsAPI = {
  list: () => axios.get(`${API_URL}/api/agents/`),
  // ...
};
```

## 📊 Monitoring et Logs

### Logs Frontend (Local)
```bash
docker-compose logs -f frontend
```

### Logs Frontend (Cloud Run)
```bash
# Logs en temps réel
gcloud run logs tail --service chatagentb-frontend --region europe-west1

# Logs avec filtre
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chatagentb-frontend"
```

### Métriques Nginx
```bash
# Accéder au container
docker exec -it chatagentb-frontend sh

# Vérifier les logs Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## 🐛 Troubleshooting

### Erreur : Cannot connect to backend

**Cause** : `VITE_API_URL` incorrect ou CORS mal configuré

**Solution** :
```bash
# Vérifier l'URL dans le code compilé
docker run chatagentb-frontend cat /usr/share/nginx/html/assets/index-*.js | grep -o "https://[^\"]*"

# Reconstruire avec la bonne URL
gcloud builds submit \
  --build-arg VITE_API_URL=https://correct-backend-url.run.app
```

### Erreur : 404 sur les routes React

**Cause** : Nginx ne redirige pas vers `index.html`

**Solution** : Vérifier la config Nginx :
```nginx
location / {
    try_files $uri $uri/ /index.html;  # ← Important pour SPA
}
```

### Erreur : Assets not cached

**Cause** : Headers Cache-Control manquants

**Solution** : Vérifier la config Nginx :
```bash
# Tester les headers
curl -I https://chatagentb-frontend-xxx.run.app/assets/index-abc.js

# Devrait retourner :
# Cache-Control: public, immutable
# Expires: <1 an dans le futur>
```

### Erreur : Health check fails

**Cause** : Endpoint `/health` non configuré

**Solution** :
```nginx
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

### Port 80 déjà utilisé (local)

**Solution** :
```powershell
# Windows : Trouver le processus
netstat -ano | findstr :80

# Tuer le processus
taskkill /PID <PID> /F

# Ou changer le port dans docker-compose.yml
ports:
  - "3000:80"  # Accès via http://localhost:3000
```

## 🎨 Optimisations Cloud Run

### 1. Réduire la taille de l'image
```dockerfile
# Utiliser Alpine
FROM nginx:alpine  # ~23 MB au lieu de ~140 MB (nginx:latest)

# Supprimer les fichiers inutiles
RUN rm -rf /usr/share/nginx/html/assets/*.map
```

### 2. Améliorer le cache
```nginx
# Cache agressif des assets avec hash
location ~* \.(js|css|png|jpg|svg|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Pas de cache pour index.html
location = /index.html {
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

### 3. Compression Gzip
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript 
           application/javascript application/json;
```

## 📚 Documentation

- [Guide complet de déploiement GCP](../DEPLOY_GCP.md)
- [Démarrage rapide GCP](../QUICKSTART_GCP.md)
- [Commandes GCP](../GCP_COMMANDS.md)
- [Vite Documentation](https://vitejs.dev/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

**Note** : Pour plus de détails sur le déploiement GCP, consultez [GCP_SETUP_COMPLETE.md](../GCP_SETUP_COMPLETE.md)
