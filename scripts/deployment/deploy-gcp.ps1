# ChatAgentB GCP Cloud Run Deployment Script
# PowerShell script for Windows

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "europe-west1"
)

Write-Host "Deploying ChatAgentB to GCP Cloud Run" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: gcloud CLI is not installed." -ForegroundColor Red
    Write-Host "   Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Configure project
Write-Host "Configuring GCP project..." -ForegroundColor Green
gcloud config set project $ProjectId

# Variables
$DB_INSTANCE = "chatagentb-db"
$DB_NAME = "chatagentb"
$DB_USER = "chatagentb"
$REDIS_INSTANCE = "chatagentb-redis"

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Project: $ProjectId" -ForegroundColor White
Write-Host "  Region: $Region" -ForegroundColor White
Write-Host ""

# Step 1: Enable required APIs
Write-Host "Step 1: Enabling GCP APIs..." -ForegroundColor Green
$apis = @(
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "sqladmin.googleapis.com",
    "redis.googleapis.com",
    "secretmanager.googleapis.com",
    "containerregistry.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "  - Enabling $api..." -ForegroundColor Gray
    gcloud services enable $api --quiet
}

Write-Host "APIs enabled successfully" -ForegroundColor Green
Write-Host ""

# Step 2: Create secrets
Write-Host "Step 2: Configuring secrets..." -ForegroundColor Green

# Django Secret Key
$djangoSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 50 | ForEach-Object {[char]$_})
Write-Host "  - Creating django-secret..." -ForegroundColor Gray
echo $djangoSecret | gcloud secrets create chatagentb-django-secret --data-file=- --replication-policy=automatic 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    WARNING: Secret chatagentb-django-secret already exists" -ForegroundColor Yellow
}

# Database Password
Write-Host "  - Enter database password:" -ForegroundColor Yellow
$dbPassword = Read-Host -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword)
)
echo $dbPasswordPlain | gcloud secrets create chatagentb-db-password --data-file=- --replication-policy=automatic 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    WARNING: Secret chatagentb-db-password already exists" -ForegroundColor Yellow
}

# OpenAI API Key
Write-Host "  - Enter your OpenAI API key:" -ForegroundColor Yellow
$openaiKey = Read-Host -AsSecureString
$openaiKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($openaiKey)
)
echo $openaiKeyPlain | gcloud secrets create chatagentb-openai-api-key --data-file=- --replication-policy=automatic 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    WARNING: Secret chatagentb-openai-api-key already exists" -ForegroundColor Yellow
}

Write-Host "Secrets configured" -ForegroundColor Green
Write-Host ""

# Step 3: Create Cloud SQL PostgreSQL
Write-Host "Step 3: Creating Cloud SQL instance..." -ForegroundColor Green
Write-Host "  Instance: $DB_INSTANCE" -ForegroundColor Gray
Write-Host "  (This may take several minutes...)" -ForegroundColor Yellow

gcloud sql instances create $DB_INSTANCE `
    --database-version=POSTGRES_15 `
    --tier=db-f1-micro `
    --region=$Region `
    --root-password=$dbPasswordPlain `
    --storage-type=SSD `
    --storage-size=10GB `
    --backup `
    --backup-start-time=03:00 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "  WARNING: Cloud SQL instance already exists or creation error" -ForegroundColor Yellow
} else {
    Write-Host "Cloud SQL instance created" -ForegroundColor Green
}

# Create database and user
Write-Host "  - Creating database..." -ForegroundColor Gray
gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE 2>$null
gcloud sql users create $DB_USER --instance=$DB_INSTANCE --password=$dbPasswordPlain 2>$null

Write-Host ""

# Step 4: Create Memorystore Redis
Write-Host "Step 4: Creating Redis instance (Memorystore)..." -ForegroundColor Green
Write-Host "  Instance: $REDIS_INSTANCE" -ForegroundColor Gray
Write-Host "  (This may take several minutes...)" -ForegroundColor Yellow

gcloud redis instances create $REDIS_INSTANCE `
    --size=1 `
    --region=$Region `
    --redis-version=redis_7_0 `
    --tier=basic 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "  WARNING: Redis instance already exists or creation error" -ForegroundColor Yellow
} else {
    Write-Host "Redis instance created" -ForegroundColor Green
}

# Get Redis IP
Write-Host "  - Retrieving Redis IP..." -ForegroundColor Gray
$redisHost = gcloud redis instances describe $REDIS_INSTANCE --region=$Region --format="value(host)"
Write-Host "  Redis IP: $redisHost" -ForegroundColor White

Write-Host ""

# Step 5: Build and deploy via Cloud Build
Write-Host "Step 5: Building and deploying services..." -ForegroundColor Green
Write-Host "  (This may take 10-15 minutes...)" -ForegroundColor Yellow

$cloudSqlConnection = "${ProjectId}:${Region}:${DB_INSTANCE}"

Write-Host "  - Submitting to Cloud Build..." -ForegroundColor Gray
gcloud builds submit `
    --config=cloudbuild.yaml `
    --substitutions="_REGION=$Region,_CLOUDSQL_INSTANCE=$cloudSqlConnection,_DB_NAME=$DB_NAME,_DB_USER=$DB_USER,_REDIS_HOST=$redisHost"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment successful!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 6: Display URLs
Write-Host "Application URLs:" -ForegroundColor Cyan
Write-Host ""

$backendUrl = gcloud run services describe chatagentb-backend --region=$Region --format="value(status.url)"
$frontendUrl = gcloud run services describe chatagentb-frontend --region=$Region --format="value(status.url)"

Write-Host "  Backend:  $backendUrl" -ForegroundColor Green
Write-Host "  Frontend: $frontendUrl" -ForegroundColor Green
Write-Host "  Admin:    $backendUrl/admin/" -ForegroundColor Green

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Configure CORS in settings.py with the frontend URL" -ForegroundColor White
Write-Host "  2. Create a superuser: gcloud run services update chatagentb-backend --update-env-vars DJANGO_SUPERUSER_USERNAME=admin,..." -ForegroundColor White
Write-Host "  3. Check logs: gcloud run logs read --service chatagentb-backend" -ForegroundColor White
Write-Host ""
Write-Host "Deployment completed successfully!" -ForegroundColor Green
