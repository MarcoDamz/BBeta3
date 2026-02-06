# Create Django Superuser - Simple PowerShell Script
# This connects to Cloud SQL via proxy and runs Django management command

Write-Host "`n════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Django Superuser Creation - Cloud SQL Proxy Method" -ForegroundColor White
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# Configuration
$PROJECT_ID = "bridgetbeta"
$INSTANCE_CONNECTION_NAME = "bridgetbeta:europe-west1:chatagentb-db"
$DB_USER = "chatagentb"
$DB_NAME = "chatagentb"
$DB_PASSWORD = "aTRtDg95o4u7MNjCXdQkJv3I"

# Superuser details
$SUPERUSER_USERNAME = "admin"
$SUPERUSER_EMAIL = "admin@admin.fr"
$SUPERUSER_PASSWORD = "3RUwJfGr14KWVv0n"

Write-Host "📋 Configuration:" -ForegroundColor Cyan
Write-Host "   Project: $PROJECT_ID" -ForegroundColor Gray
Write-Host "   Database: $DB_NAME" -ForegroundColor Gray
Write-Host "   Superuser: $SUPERUSER_USERNAME" -ForegroundColor Gray
Write-Host ""

# Check if cloud-sql-proxy is installed
Write-Host "🔍 Checking for cloud-sql-proxy..." -ForegroundColor Yellow
$proxyPath = Get-Command cloud-sql-proxy -ErrorAction SilentlyContinue

if (-not $proxyPath) {
    Write-Host "❌ cloud-sql-proxy not found!" -ForegroundColor Red
    Write-Host "`n📥 Please install it:" -ForegroundColor Yellow
    Write-Host "   1. Download from: https://cloud.google.com/sql/docs/postgres/connect-admin-proxy" -ForegroundColor White
    Write-Host "   2. Or use: gcloud components install cloud-sql-proxy" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ cloud-sql-proxy found at: $($proxyPath.Source)" -ForegroundColor Green
Write-Host ""

# Start Cloud SQL Proxy
Write-Host "🚀 Starting Cloud SQL Proxy..." -ForegroundColor Yellow
$proxyJob = Start-Job -ScriptBlock {
    param($connectionName)
    cloud-sql-proxy $connectionName
} -ArgumentList $INSTANCE_CONNECTION_NAME

Write-Host "⏳ Waiting for proxy to start (5 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Check if proxy is running
$proxyRunning = Get-Job -Id $proxyJob.Id | Where-Object { $_.State -eq "Running" }
if (-not $proxyRunning) {
    Write-Host "❌ Cloud SQL Proxy failed to start!" -ForegroundColor Red
    Receive-Job -Id $proxyJob.Id
    Remove-Job -Id $proxyJob.Id -Force
    exit 1
}

Write-Host "✅ Cloud SQL Proxy is running!" -ForegroundColor Green
Write-Host ""

# Create Python script to create superuser
Write-Host "📝 Creating superuser via Django ORM..." -ForegroundColor Yellow

$pythonScript = @"
import os
os.environ['POSTGRES_HOST'] = '127.0.0.1'
os.environ['POSTGRES_PORT'] = '5432'
os.environ['POSTGRES_DB'] = '$DB_NAME'
os.environ['POSTGRES_USER'] = '$DB_USER'
os.environ['POSTGRES_PASSWORD'] = '$DB_PASSWORD'
os.environ['SECRET_KEY'] = 'temporary-key-for-superuser-creation'
os.environ['DEBUG'] = 'False'

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = '$SUPERUSER_USERNAME'
email = '$SUPERUSER_EMAIL'
password = '$SUPERUSER_PASSWORD'

if User.objects.filter(username=username).exists():
    print('⚠️  User already exists!')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'✅ Password updated for user: {username}')
else:
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superuser created: {username}')
"@

try {
    # Change to backend directory
    Push-Location -Path "backend"
    
    # Run Python script
    $pythonScript | python -
    
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  ✅ SUPERUSER CREATION COMPLETE!" -ForegroundColor Green
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔑 Login Credentials:" -ForegroundColor Cyan
    Write-Host "   URL:      https://chatagentb-backend-548740531838.europe-west1.run.app/admin/" -ForegroundColor White
    Write-Host "   Username: $SUPERUSER_USERNAME" -ForegroundColor White
    Write-Host "   Password: $SUPERUSER_PASSWORD" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "❌ Error creating superuser:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
} finally {
    # Cleanup
    Pop-Location
    Write-Host "🧹 Stopping Cloud SQL Proxy..." -ForegroundColor Gray
    Stop-Job -Id $proxyJob.Id
    Remove-Job -Id $proxyJob.Id -Force
    Write-Host "✅ Cleanup complete!" -ForegroundColor Green
}
