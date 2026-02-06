#!/bin/bash
# Script de déploiement ChatAgentB sur GCP Cloud Run
# Bash script pour Linux/Mac

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables
PROJECT_ID=${1:-""}
REGION=${2:-"europe-west1"}

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Erreur: PROJECT_ID requis${NC}"
    echo "Usage: ./deploy-gcp.sh <PROJECT_ID> [REGION]"
    echo "Exemple: ./deploy-gcp.sh mon-chatagentb-project europe-west1"
    exit 1
fi

echo -e "${CYAN}🚀 Déploiement de ChatAgentB sur GCP Cloud Run${NC}"
echo "================================================"
echo ""

# Vérifier que gcloud est installé
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Erreur: gcloud CLI n'est pas installé.${NC}"
    echo -e "${YELLOW}   Installez-le depuis: https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Configuration du projet
echo -e "${GREEN}📦 Configuration du projet GCP...${NC}"
gcloud config set project $PROJECT_ID

# Variables
DB_INSTANCE="chatagentb-db"
DB_NAME="chatagentb"
DB_USER="chatagentb"
REDIS_INSTANCE="chatagentb-redis"

echo ""
echo -e "${CYAN}Configuration:${NC}"
echo -e "  Projet: ${PROJECT_ID}"
echo -e "  Région: ${REGION}"
echo ""

# Étape 1: Activer les APIs nécessaires
echo -e "${GREEN}🔧 Activation des APIs GCP...${NC}"
APIS=(
    "run.googleapis.com"
    "cloudbuild.googleapis.com"
    "sqladmin.googleapis.com"
    "redis.googleapis.com"
    "secretmanager.googleapis.com"
    "containerregistry.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo -e "  • Activation de ${api}..."
    gcloud services enable $api --quiet
done

echo -e "${GREEN}✅ APIs activées avec succès${NC}"
echo ""

# Étape 2: Créer les secrets
echo -e "${GREEN}🔐 Configuration des secrets...${NC}"

# Secret Key Django
DJANGO_SECRET=$(openssl rand -base64 50 | tr -d "=+/" | cut -c1-50)
echo -e "  • Création du secret django-secret..."
echo -n "$DJANGO_SECRET" | gcloud secrets create django-secret --data-file=- --replication-policy=automatic 2>/dev/null || echo -e "    ${YELLOW}⚠️  Secret django-secret existe déjà${NC}"

# Mot de passe DB
echo -e "  ${YELLOW}• Entrez le mot de passe de la base de données:${NC}"
read -s DB_PASSWORD
echo -n "$DB_PASSWORD" | gcloud secrets create db-password --data-file=- --replication-policy=automatic 2>/dev/null || echo -e "    ${YELLOW}⚠️  Secret db-password existe déjà${NC}"

# OpenAI API Key
echo -e "  ${YELLOW}• Entrez votre clé API OpenAI:${NC}"
read -s OPENAI_KEY
echo -n "$OPENAI_KEY" | gcloud secrets create openai-api-key --data-file=- --replication-policy=automatic 2>/dev/null || echo -e "    ${YELLOW}⚠️  Secret openai-api-key existe déjà${NC}"

echo -e "${GREEN}✅ Secrets configurés${NC}"
echo ""

# Étape 3: Créer Cloud SQL PostgreSQL
echo -e "${GREEN}🗄️  Création de l'instance Cloud SQL...${NC}"
echo -e "  Instance: ${DB_INSTANCE}"
echo -e "  ${YELLOW}(Cela peut prendre plusieurs minutes...)${NC}"

gcloud sql instances create $DB_INSTANCE \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=$REGION \
    --root-password="$DB_PASSWORD" \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup \
    --backup-start-time=03:00 2>/dev/null || echo -e "  ${YELLOW}⚠️  Instance Cloud SQL existe déjà ou erreur de création${NC}"

# Créer la base de données et l'utilisateur
echo -e "  • Création de la base de données..."
gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE 2>/dev/null || true
gcloud sql users create $DB_USER --instance=$DB_INSTANCE --password="$DB_PASSWORD" 2>/dev/null || true

echo ""

# Étape 4: Créer Memorystore Redis
echo -e "${GREEN}💾 Création de l'instance Redis (Memorystore)...${NC}"
echo -e "  Instance: ${REDIS_INSTANCE}"
echo -e "  ${YELLOW}(Cela peut prendre plusieurs minutes...)${NC}"

gcloud redis instances create $REDIS_INSTANCE \
    --size=1 \
    --region=$REGION \
    --redis-version=redis_7_0 \
    --tier=basic 2>/dev/null || echo -e "  ${YELLOW}⚠️  Instance Redis existe déjà ou erreur de création${NC}"

# Récupérer l'IP Redis
echo -e "  • Récupération de l'IP Redis..."
REDIS_HOST=$(gcloud redis instances describe $REDIS_INSTANCE --region=$REGION --format="value(host)")
echo -e "  IP Redis: ${REDIS_HOST}"

echo ""

# Étape 5: Construction et déploiement via Cloud Build
echo -e "${GREEN}🏗️  Construction et déploiement des services...${NC}"
echo -e "  ${YELLOW}(Cela peut prendre 10-15 minutes...)${NC}"

CLOUDSQL_CONNECTION="${PROJECT_ID}:${REGION}:${DB_INSTANCE}"

echo -e "  • Soumission à Cloud Build..."
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions="_REGION=$REGION,_CLOUDSQL_INSTANCE=$CLOUDSQL_CONNECTION,_DB_NAME=$DB_NAME,_DB_USER=$DB_USER,_REDIS_HOST=$REDIS_HOST"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Déploiement réussi!${NC}"
else
    echo -e "${RED}❌ Erreur lors du déploiement${NC}"
    exit 1
fi

echo ""

# Étape 6: Afficher les URLs
echo -e "${CYAN}🌐 URLs de l'application:${NC}"
echo ""

BACKEND_URL=$(gcloud run services describe chatagentb-backend --region=$REGION --format="value(status.url)")
FRONTEND_URL=$(gcloud run services describe chatagentb-frontend --region=$REGION --format="value(status.url)")

echo -e "  ${GREEN}Backend:  ${BACKEND_URL}${NC}"
echo -e "  ${GREEN}Frontend: ${FRONTEND_URL}${NC}"
echo -e "  ${GREEN}Admin:    ${BACKEND_URL}/admin/${NC}"

echo ""
echo -e "${CYAN}📋 Prochaines étapes:${NC}"
echo -e "  1. Configurez le CORS dans settings.py avec l'URL frontend"
echo -e "  2. Créez un superuser via Cloud Run"
echo -e "  3. Consultez les logs: gcloud run logs read --service chatagentb-backend"
echo ""
echo -e "${GREEN}🎉 Déploiement terminé avec succès!${NC}"
