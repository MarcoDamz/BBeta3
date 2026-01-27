# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app

# Installation des dépendances
COPY package.json package-lock.json* ./
RUN npm install

# Copie du code source
COPY . .

# Build de production
RUN npm run build

# Stage 2: Production avec Nginx
FROM nginx:alpine

# Copie des fichiers build
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
