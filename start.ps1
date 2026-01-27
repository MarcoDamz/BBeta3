# Script de démarrage rapide pour ChatAgentB# Script de démarrage rapide pour ChatAgentB

# Windows PowerShell# Windows PowerShell



Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ChatAgentB - Démarrage Rapide" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""

# Vérifier si Docker est installé# Vérifier si Docker est installé

try {
    docker --version | Out-Null
    Write-Host "✓ Docker détecté" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host "  Installez Docker Desktop depuis: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1 
}

# Vérifier si le fichier .env existe# Vérifier si le fichier .env existe
if (-Not (Test-Path ".env")) {
    Write-Host "✗ Fichier .env manquant" -ForegroundColor Red
    Write-Host "  Copie de .env.example vers .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "  ⚠ IMPORTANT: Éditez le fichier .env et renseignez votre clé API!" -ForegroundColor Yellow
    Write-Host "    - OPENAI_API_KEY" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "  Avez-vous configuré vos clés API? (o/n)"
    if ($response -ne "o") {
        Write-Host "  Veuillez configurer .env avant de continuer." -ForegroundColor Red
        exit 1      
    }
}



Write-Host "" -ForegroundColor Cyan
Write-Host ""

Write-Host "Démarrage des services Docker..." -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan

# Construire et démarrer les services# Construire et démarrer les services

docker-compose up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   ✓ Application démarrée avec succès!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Accès à l'application:" -ForegroundColor Cyan
    Write-Host "  • Frontend:    http://localhost:3000" -ForegroundColor White
    Write-Host "  • Backend API: http://localhost:8000/api/" -ForegroundColor White
    Write-Host "  • Admin Django: http://localhost:8000/admin/" -ForegroundColor White
    Write-Host "" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Identifiants par défaut:" -ForegroundColor Cyan
    Write-Host "  • Username: admin" -ForegroundColor White
    Write-Host "  • Password: admin123" -ForegroundColor White
    Write-Host "" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commandes utiles:" -ForegroundColor Cyan    Write-Host "Commandes utiles:" -ForegroundColor Cyan
    Write-Host "  • Voir les logs:     docker-compose logs -f" -ForegroundColor White
    Write-Host "  • Arrêter:           docker-compose down" -ForegroundColor White
    Write-Host "  • Redémarrer:        docker-compose restart" -ForegroundColor White
    Write-Host "" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✗ Erreur lors du démarrage" -ForegroundColor Red
    Write-Host "  Consultez les logs: docker-compose logs" -ForegroundColor Yellow

    exit 1

}

