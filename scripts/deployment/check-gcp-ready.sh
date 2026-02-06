#!/bin/bash
#
# Verification script for GCP deployment prerequisites
# Checks all requirements before deploying ChatAgentB to GCP Cloud Run
#
# Usage:
#   ./check-gcp-ready.sh
#   ./check-gcp-ready.sh PROJECT_ID
#

set -e

PROJECT_ID="$1"
ERRORS=0
WARNINGS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

write_success() {
    echo -e "${GREEN}  $1${NC}"
}

write_error() {
    echo -e "${RED}  $1${NC}"
    ((ERRORS++))
}

write_warning() {
    echo -e "${YELLOW}  $1${NC}"
    ((WARNINGS++))
}

test_requirement() {
    local name="$1"
    local test_cmd="$2"
    local success_msg="$3"
    local error_msg="$4"
    local critical="${5:-true}"
    
    echo -ne "${GRAY}  - $name...${NC}"
    
    if eval "$test_cmd"; then
        echo -e " ${GREEN}OK${NC}"
        if [ -n "$success_msg" ]; then
            echo -e "    ${GRAY}$success_msg${NC}"
        fi
        return 0
    else
        if [ "$critical" = "true" ]; then
            echo -e " ${RED}ERROR${NC}"
            echo -e "    ${RED}$error_msg${NC}"
            ((ERRORS++))
        else
            echo -e " ${YELLOW}WARNING${NC}"
            echo -e "    ${YELLOW}$error_msg${NC}"
            ((WARNINGS++))
        fi
        return 1
    fi
}

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  GCP Deployment Readiness Check${NC}"
echo -e "${CYAN}  ChatAgentB Project${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# 1. Check tools
echo -e "${CYAN}1. Required Tools${NC}"
echo ""

test_requirement "Google Cloud SDK (gcloud)" "command -v gcloud >/dev/null 2>&1" \
    "Installed" \
    "gcloud CLI is not installed. Install from: https://cloud.google.com/sdk/docs/install"

test_requirement "Docker" "command -v docker >/dev/null 2>&1" \
    "Installed" \
    "Docker is not installed (optional for local tests)" \
    false

echo ""

# 2. Check GCP configuration
echo -e "${CYAN}2. GCP Configuration${NC}"
echo ""

CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")

if [ -n "$PROJECT_ID" ] && [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo -ne "${GRAY}  - GCP Project configured...${NC}"
    echo -e " ${YELLOW}WARNING${NC}"
    echo -e "    ${YELLOW}Current project: $CURRENT_PROJECT, requested: $PROJECT_ID${NC}"
    ((WARNINGS++))
fi

test_requirement "GCP Project configured" "[ -n \"$CURRENT_PROJECT\" ]" \
    "Active project: $CURRENT_PROJECT" \
    "No GCP project configured. Use: gcloud config set project YOUR_PROJECT_ID"

test_requirement "GCP Authentication" \
    "gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null | grep -q ." \
    "Authenticated" \
    "Not authenticated to GCP. Use: gcloud auth login"

echo ""

# 3. Check required files
echo -e "${CYAN}3. Required Files${NC}"
echo ""

REQUIRED_FILES=(
    "backend/Dockerfile.cloudrun"
    "backend/Dockerfile.worker"
    "backend/docker-entrypoint-cloudrun.sh"
    "backend/requirements.txt"
    "backend/manage.py"
    "frontend/Dockerfile.cloudrun"
    "frontend/docker-entrypoint-cloudrun.sh"
    "frontend/nginx.cloudrun.conf"
    "cloudbuild.yaml"
    ".env"
)

for file in "${REQUIRED_FILES[@]}"; do
    test_requirement "File: $file" "[ -f \"$file\" ]" \
        "" \
        "File not found: $file"
done

echo ""

# 4. Check .env file content
echo -e "${CYAN}4. Environment Configuration${NC}"
echo ""

if [ -f ".env" ]; then
    ENV_CONTENT=$(cat .env)
    
    check_env_var() {
        local var_name="$1"
        local pattern="$2"
        local description="$3"
        local critical="${4:-true}"
        
        if echo "$ENV_CONTENT" | grep -qE "$pattern"; then
            test_requirement "$var_name" "true" "$description" "" "$critical"
        else
            test_requirement "$var_name" "false" "$description" "Missing or empty: $var_name" "$critical"
        fi
    }
    
    check_env_var "POSTGRES_DB" "POSTGRES_DB=\w+" "Database name"
    check_env_var "POSTGRES_USER" "POSTGRES_USER=\w+" "Database user"
    check_env_var "POSTGRES_PASSWORD" "POSTGRES_PASSWORD=.+" "Database password"
    check_env_var "DJANGO_SECRET_KEY" "DJANGO_SECRET_KEY=.+" "Django secret key"
    check_env_var "OPENAI_API_KEY" "OPENAI_API_KEY=sk-.+" "OpenAI API key (or comment if unused)" false
fi

echo ""

# 5. Check GCP APIs (if authenticated)
if [ -n "$CURRENT_PROJECT" ]; then
    echo -e "${CYAN}5. GCP APIs (will be enabled during deployment)${NC}"
    echo ""
    
    REQUIRED_APIS=(
        "run.googleapis.com"
        "sqladmin.googleapis.com"
        "redis.googleapis.com"
        "secretmanager.googleapis.com"
        "cloudbuild.googleapis.com"
        "containerregistry.googleapis.com"
    )
    
    echo -e "${GRAY}  Checking enabled APIs...${NC}"
    ENABLED_APIS=$(gcloud services list --enabled --format="value(config.name)" 2>/dev/null || echo "")
    
    for api in "${REQUIRED_APIS[@]}"; do
        if echo "$ENABLED_APIS" | grep -q "^$api$"; then
            echo -ne "${GRAY}  - $api${NC}"
            echo -e " ${GREEN}OK${NC}"
        else
            echo -ne "${GRAY}  - $api${NC}"
            echo -e " ${YELLOW}NOT ENABLED${NC}"
            echo -e "    ${GRAY}(Will be enabled by deploy-gcp.sh)${NC}"
        fi
    done
    
    echo ""
    
    # 6. Check secrets (if they exist)
    echo -e "${CYAN}6. GCP Secrets (will be created during deployment)${NC}"
    echo ""
    
    REQUIRED_SECRETS=(
        "chatagentb-django-secret"
        "chatagentb-db-password"
        "chatagentb-openai-api-key"
    )
    
    for secret in "${REQUIRED_SECRETS[@]}"; do
        if gcloud secrets describe "$secret" --format="value(name)" >/dev/null 2>&1; then
            echo -ne "${GRAY}  - $secret${NC}"
            echo -e " ${GREEN}EXISTS${NC}"
        else
            echo -ne "${GRAY}  - $secret${NC}"
            echo -e " ${YELLOW}NOT FOUND${NC}"
            echo -e "    ${GRAY}(Will be created by deploy-gcp.sh)${NC}"
        fi
    done
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Summary${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}ALL CHECKS PASSED!${NC}"
    echo ""
    echo -e "${GREEN}You are ready to deploy to GCP Cloud Run!${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo -e "  1. Review your .env file (especially API keys)"
    echo -e "  2. Run: ./deploy-gcp.sh"
    echo ""
    echo -e "${CYAN}Documentation:${NC}"
    echo -e "  - Quick start: QUICKSTART_GCP.md"
    echo -e "  - Full guide: DEPLOY_GCP.md"
    echo -e "  - Commands: GCP_COMMANDS.md"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}CHECKS PASSED WITH WARNINGS${NC}"
    echo ""
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo ""
    echo -e "${YELLOW}You can proceed with deployment, but review the warnings above.${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo -e "  1. Review warnings above"
    echo -e "  2. Review your .env file (especially API keys)"
    echo -e "  3. Run: ./deploy-gcp.sh"
    echo ""
    exit 0
else
    echo -e "${RED}CHECKS FAILED${NC}"
    echo ""
    echo -e "${RED}Errors: $ERRORS${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo ""
    echo -e "${RED}Please fix the errors above before deploying.${NC}"
    echo ""
    echo -e "${CYAN}Documentation:${NC}"
    echo -e "  - Setup guide: START_HERE_GCP.md"
    echo -e "  - Full guide: DEPLOY_GCP.md"
    echo ""
    exit 1
fi
