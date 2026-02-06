# Script pour créer un superuser Django sur Cloud Run
# Create Django Superuser on Cloud Run

Write-Host "`n=== CREATE DJANGO SUPERUSER ===" -ForegroundColor Cyan
Write-Host "This script will help you create a Django admin superuser`n" -ForegroundColor Gray

# Project configuration
$PROJECT_ID = "bridgetbeta"
$REGION = "europe-west1"
$SERVICE = "chatagentb-backend"

Write-Host "? Connecting to Cloud Run service: $SERVICE" -ForegroundColor Yellow
Write-Host "  This will open a proxy connection...`n" -ForegroundColor Gray

# Option 1: Using environment variables (recommended for automation)
Write-Host "=== OPTION 1: Automatic Creation (via environment variables) ===" -ForegroundColor Green
Write-Host "Set these environment variables on the backend service:`n" -ForegroundColor Gray

$username = Read-Host "Enter superuser username (default: admin)"
if ([string]::IsNullOrWhiteSpace($username)) { $username = "admin" }

$email = Read-Host "Enter superuser email (default: admin@example.com)"
if ([string]::IsNullOrWhiteSpace($email)) { $email = "admin@example.com" }

Write-Host "`nGenerating secure password..." -ForegroundColor Yellow
$password = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})
Write-Host "Generated password: $password" -ForegroundColor Green
Write-Host "(Save this password securely!)`n" -ForegroundColor Red

Write-Host "Command to update service with superuser creation:" -ForegroundColor Cyan
Write-Host "gcloud run services update $SERVICE ``" -ForegroundColor White
Write-Host "  --region=$REGION ``" -ForegroundColor White
Write-Host "  --project=$PROJECT_ID ``" -ForegroundColor White
Write-Host "  --update-env-vars DJANGO_SUPERUSER_USERNAME=$username,DJANGO_SUPERUSER_EMAIL=$email,DJANGO_SUPERUSER_PASSWORD=$password" -ForegroundColor White

Write-Host "`n`n=== OPTION 2: Manual Creation (via shell) ===" -ForegroundColor Green
Write-Host "If you prefer interactive creation:`n" -ForegroundColor Gray

Write-Host "1. Start a Cloud Run proxy:" -ForegroundColor Yellow
Write-Host "   gcloud run services proxy $SERVICE --region=$REGION --project=$PROJECT_ID`n" -ForegroundColor White

Write-Host "2. In another terminal, connect to the container:" -ForegroundColor Yellow
Write-Host "   gcloud run services exec $SERVICE --region=$REGION --project=$PROJECT_ID -- /bin/bash`n" -ForegroundColor White

Write-Host "3. Inside the container, run:" -ForegroundColor Yellow
Write-Host "   python manage.py createsuperuser`n" -ForegroundColor White

Write-Host "`n=== OPTION 3: Using Cloud Run Jobs (recommended) ===" -ForegroundColor Green
Write-Host "Create a one-time job to run the command:`n" -ForegroundColor Gray

Write-Host "gcloud run jobs create create-superuser ``" -ForegroundColor White
Write-Host "  --image=gcr.io/$PROJECT_ID/chatagentb-backend:latest ``" -ForegroundColor White
Write-Host "  --region=$REGION ``" -ForegroundColor White
Write-Host "  --set-cloudsql-instances=bridgetbeta:europe-west1:chatagentb-db ``" -ForegroundColor White
Write-Host "  --set-secrets=SECRET_KEY=chatagentb-django-secret:latest,POSTGRES_PASSWORD=chatagentb-db-password:4 ``" -ForegroundColor White
Write-Host "  --set-env-vars=DJANGO_SUPERUSER_USERNAME=$username,DJANGO_SUPERUSER_EMAIL=$email,DJANGO_SUPERUSER_PASSWORD=$password ``" -ForegroundColor White
Write-Host "  --command=python ``" -ForegroundColor White
Write-Host "  --args=manage.py,createsuperuser,--noinput`n" -ForegroundColor White

Write-Host "Then execute the job:" -ForegroundColor Yellow
Write-Host "gcloud run jobs execute create-superuser --region=$REGION --project=$PROJECT_ID`n" -ForegroundColor White

Write-Host "`n=== RECOMMENDED APPROACH ===" -ForegroundColor Magenta
Write-Host "Use Option 3 (Cloud Run Jobs) - it's the cleanest approach!`n" -ForegroundColor White

$choice = Read-Host "Would you like to create the job now? (y/n)"
if ($choice -eq "y" -or $choice -eq "Y") {
    Write-Host "`nCreating Cloud Run Job..." -ForegroundColor Yellow
    
    gcloud run jobs create create-superuser `
        --image="gcr.io/$PROJECT_ID/chatagentb-backend:latest" `
        --region=$REGION `
        --project=$PROJECT_ID `
        --set-cloudsql-instances="bridgetbeta:europe-west1:chatagentb-db" `
        --set-secrets="SECRET_KEY=chatagentb-django-secret:latest,POSTGRES_PASSWORD=chatagentb-db-password:4,OPENAI_API_KEY=chatagentb-openai-api-key:latest" `
        --set-env-vars="DEBUG=False,POSTGRES_HOST=/cloudsql/bridgetbeta:europe-west1:chatagentb-db,POSTGRES_DB=chatagentb,POSTGRES_USER=chatagentb,DJANGO_SUPERUSER_USERNAME=$username,DJANGO_SUPERUSER_EMAIL=$email,DJANGO_SUPERUSER_PASSWORD=$password" `
        --command=python `
        --args=manage.py,createsuperuser,--noinput
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n? Job created successfully!" -ForegroundColor Green
        Write-Host "Executing job..." -ForegroundColor Yellow
        
        gcloud run jobs execute create-superuser --region=$REGION --project=$PROJECT_ID --wait
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n? Superuser created successfully!" -ForegroundColor Green
            Write-Host "`nLogin credentials:" -ForegroundColor Cyan
            Write-Host "  Username: $username" -ForegroundColor White
            Write-Host "  Password: $password" -ForegroundColor White
            Write-Host "  Email: $email" -ForegroundColor White
            Write-Host "`nAdmin URL: https://chatagentb-backend-548740531838.europe-west1.run.app/admin/" -ForegroundColor Cyan
        } else {
            Write-Host "`n? Job execution failed" -ForegroundColor Red
        }
    } else {
        Write-Host "`n? Job creation failed" -ForegroundColor Red
    }
} else {
    Write-Host "`nOK - You can create the superuser manually later." -ForegroundColor Gray
}

Write-Host "`n=== DONE ===" -ForegroundColor Green
