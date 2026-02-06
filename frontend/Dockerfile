FROM node:20-alpine as builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

# En développement, on ne fait PAS "RUN npm run build"
# On ne copie PAS le code ici si on utilise les volumes dans docker-compose
COPY . .

EXPOSE 3000

# On lance le serveur de développement de Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]