# Script pour créer les groupes d'utilisateurs

Write-Host "🔧 Création des groupes d'utilisateurs..." -ForegroundColor Cyan
Write-Host ""

docker-compose exec backend python manage.py create_user_groups

Write-Host ""
Write-Host "✅ Groupes créés avec succès !" -ForegroundColor Green
Write-Host ""
Write-Host "Groupes disponibles :" -ForegroundColor Yellow
Write-Host "  - Standard Users : Utilisateurs normaux (pas d'accès admin)" -ForegroundColor White
Write-Host "  - Administrators : Administrateurs (accès complet)" -ForegroundColor White
Write-Host ""
Write-Host "Les nouveaux utilisateurs sont automatiquement assignés au groupe 'Standard Users'" -ForegroundColor Cyan
