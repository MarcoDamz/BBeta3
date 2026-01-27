# Script d'arrêt pour ChatAgentB
# Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ChatAgentB - Arrêt des Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Arrêt des services Docker..." -ForegroundColor Yellow

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Services arrêtés avec succès!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour supprimer également les volumes (données):" -ForegroundColor Cyan
    Write-Host "  docker-compose down -v" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Erreur lors de l'arrêt" -ForegroundColor Red
    exit 1
}
