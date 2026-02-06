<#
.SYNOPSIS
    Verification script for GCP deployment prerequisites

.DESCRIPTION
    Checks all requirements before deploying ChatAgentB to GCP Cloud Run

.PARAMETER ProjectId
    GCP Project ID (optional)

.EXAMPLE
    .\check-gcp-ready.ps1
    .\check-gcp-ready.ps1 -ProjectId "my-gcp-project"
#>

param(
    [string]$ProjectId
)

$ErrorActionPreference = "Stop"
$script:errors = 0
$script:warnings = 0

function Write-Success {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor Red
    $script:errors++
}

function Write-Warning {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor Yellow
    $script:warnings++
}

function Test-Requirement {
    param(
        [string]$Name,
        [scriptblock]$Test,
        [string]$SuccessMessage,
        [string]$ErrorMessage,
        [bool]$Critical = $true
    )
    
    Write-Host "  - $Name..." -NoNewline -ForegroundColor Gray
    
    try {
        $result = & $Test
        if ($result) {
            Write-Host " OK" -ForegroundColor Green
            if ($SuccessMessage) {
                Write-Host "    $SuccessMessage" -ForegroundColor DarkGray
            }
            return $true
        } else {
            if ($Critical) {
                Write-Host " ERROR" -ForegroundColor Red
                Write-Host "    $ErrorMessage" -ForegroundColor Red
                $script:errors++
            } else {
                Write-Host " WARNING" -ForegroundColor Yellow
                Write-Host "    $ErrorMessage" -ForegroundColor Yellow
                $script:warnings++
            }
            return $false
        }
    } catch {
        if ($Critical) {
            Write-Host " ERROR" -ForegroundColor Red
            Write-Host "    $ErrorMessage" -ForegroundColor Red
            $script:errors++
        } else {
            Write-Host " WARNING" -ForegroundColor Yellow
            Write-Host "    $ErrorMessage" -ForegroundColor Yellow
            $script:warnings++
        }
        return $false
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GCP Deployment Readiness Check" -ForegroundColor Cyan
Write-Host "  ChatAgentB Project" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check tools
Write-Host "1. Required Tools" -ForegroundColor Cyan
Write-Host ""

Test-Requirement `
    -Name "Google Cloud SDK (gcloud)" `
    -Test { Get-Command gcloud -ErrorAction SilentlyContinue } `
    -SuccessMessage "Installed" `
    -ErrorMessage "gcloud CLI is not installed. Install from: https://cloud.google.com/sdk/docs/install"

Test-Requirement `
    -Name "Docker" `
    -Test { Get-Command docker -ErrorAction SilentlyContinue } `
    -SuccessMessage "Installed" `
    -ErrorMessage "Docker is not installed (optional for local tests)" `
    -Critical $false

Write-Host ""

# 2. Check GCP configuration
Write-Host "2. GCP Configuration" -ForegroundColor Cyan
Write-Host ""

$currentProject = ""
try {
    $currentProject = (gcloud config get-value project 2>$null)
    if ($currentProject) {
        $currentProject = $currentProject.Trim()
    }
} catch {}

if ($ProjectId -and $currentProject -ne $ProjectId) {
    Write-Host "  - GCP Project configured..." -NoNewline -ForegroundColor Gray
    Write-Host " WARNING" -ForegroundColor Yellow
    Write-Host "    Current project: $currentProject, requested: $ProjectId" -ForegroundColor Yellow
    $warnings++
}

Test-Requirement `
    -Name "GCP Project configured" `
    -Test { ![string]::IsNullOrWhiteSpace($currentProject) } `
    -SuccessMessage "Active project: $currentProject" `
    -ErrorMessage "No GCP project configured. Use: gcloud config set project YOUR_PROJECT_ID"

Test-Requirement `
    -Name "GCP Authentication" `
    -Test { 
        $authList = (gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>$null)
        ![string]::IsNullOrWhiteSpace($authList)
    } `
    -SuccessMessage "Authenticated" `
    -ErrorMessage "Not authenticated to GCP. Use: gcloud auth login"

Write-Host ""

# 3. Check required files
Write-Host "3. Required Files" -ForegroundColor Cyan
Write-Host ""

$requiredFiles = @(
    "backend/Dockerfile.cloudrun",
    "backend/Dockerfile.worker",
    "backend/docker-entrypoint-cloudrun.sh",
    "backend/requirements.txt",
    "backend/manage.py",
    "frontend/Dockerfile.cloudrun",
    "frontend/docker-entrypoint-cloudrun.sh",
    "frontend/nginx.cloudrun.conf",
    "cloudbuild.yaml",
    ".env"
)

foreach ($file in $requiredFiles) {
    Test-Requirement `
        -Name "File: $file" `
        -Test { Test-Path $file } `
        -SuccessMessage "" `
        -ErrorMessage "File not found: $file"
}

Write-Host ""

# 4. Check .env file content
Write-Host "4. Environment Configuration" -ForegroundColor Cyan
Write-Host ""

if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    $requiredEnvVars = @(
        @{Name="POSTGRES_DB"; Pattern="POSTGRES_DB=\w+"; Description="Database name"},
        @{Name="POSTGRES_USER"; Pattern="POSTGRES_USER=\w+"; Description="Database user"},
        @{Name="POSTGRES_PASSWORD"; Pattern="POSTGRES_PASSWORD=.+"; Description="Database password"},
        @{Name="DJANGO_SECRET_KEY"; Pattern="DJANGO_SECRET_KEY=.+"; Description="Django secret key"},
        @{Name="OPENAI_API_KEY"; Pattern="OPENAI_API_KEY=sk-.+"; Description="OpenAI API key (or comment if unused)"}
    )
    
    foreach ($var in $requiredEnvVars) {
        $found = $envContent -match $var.Pattern
        Test-Requirement `
            -Name "$($var.Name)" `
            -Test { $found } `
            -SuccessMessage "$($var.Description)" `
            -ErrorMessage "Missing or empty: $($var.Name)" `
            -Critical ($var.Name -ne "OPENAI_API_KEY")
    }
}

Write-Host ""

# 5. Check GCP APIs (if authenticated)
if (![string]::IsNullOrWhiteSpace($currentProject)) {
    Write-Host "5. GCP APIs (will be enabled during deployment)" -ForegroundColor Cyan
    Write-Host ""
    
    $requiredApis = @(
        "run.googleapis.com",
        "sqladmin.googleapis.com",
        "redis.googleapis.com",
        "secretmanager.googleapis.com",
        "cloudbuild.googleapis.com",
        "containerregistry.googleapis.com"
    )
    
    Write-Host "  Checking enabled APIs..." -ForegroundColor Gray
    $enabledApis = @()
    try {
        $apiList = (gcloud services list --enabled --format="value(config.name)" 2>$null)
        if ($apiList) {
            $enabledApis = $apiList -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ }
        }
    } catch {}
    
    foreach ($api in $requiredApis) {
        $enabled = $enabledApis -contains $api
        if ($enabled) {
            Write-Host "  - $api" -NoNewline -ForegroundColor Gray
            Write-Host " OK" -ForegroundColor Green
        } else {
            Write-Host "  - $api" -NoNewline -ForegroundColor Gray
            Write-Host " NOT ENABLED" -ForegroundColor Yellow
            Write-Host "    (Will be enabled by deploy-gcp.ps1)" -ForegroundColor DarkGray
        }
    }
    
    Write-Host ""
    
    # 6. Check secrets (if they exist)
    Write-Host "6. GCP Secrets (will be created during deployment)" -ForegroundColor Cyan
    Write-Host ""
    
    $requiredSecrets = @(
        "chatagentb-django-secret",
        "chatagentb-db-password",
        "chatagentb-openai-api-key"
    )
    
    foreach ($secret in $requiredSecrets) {
        try {
            $secretExists = $null -ne (gcloud secrets describe $secret --format="value(name)" 2>$null)
            if ($secretExists) {
                Write-Host "  - $secret" -NoNewline -ForegroundColor Gray
                Write-Host " EXISTS" -ForegroundColor Green
            } else {
                Write-Host "  - $secret" -NoNewline -ForegroundColor Gray
                Write-Host " NOT FOUND" -ForegroundColor Yellow
                Write-Host "    (Will be created by deploy-gcp.ps1)" -ForegroundColor DarkGray
            }
        } catch {
            Write-Host "  - $secret" -NoNewline -ForegroundColor Gray
            Write-Host " NOT FOUND" -ForegroundColor Yellow
            Write-Host "    (Will be created by deploy-gcp.ps1)" -ForegroundColor DarkGray
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($script:errors -eq 0 -and $script:warnings -eq 0) {
    Write-Host "ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You are ready to deploy to GCP Cloud Run!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review your .env file (especially API keys)" -ForegroundColor White
    Write-Host "  2. Run: .\deploy-gcp.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Documentation:" -ForegroundColor Cyan
    Write-Host "  - Quick start: QUICKSTART_GCP.md" -ForegroundColor White
    Write-Host "  - Full guide: DEPLOY_GCP.md" -ForegroundColor White
    Write-Host "  - Commands: GCP_COMMANDS.md" -ForegroundColor White
    Write-Host ""
    exit 0
} elseif ($script:errors -eq 0) {
    Write-Host "CHECKS PASSED WITH WARNINGS" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Warnings: $script:warnings" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can proceed with deployment, but review the warnings above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review warnings above" -ForegroundColor White
    Write-Host "  2. Review your .env file (especially API keys)" -ForegroundColor White
    Write-Host "  3. Run: .\deploy-gcp.ps1" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host "CHECKS FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Errors: $script:errors" -ForegroundColor Red
    Write-Host "Warnings: $script:warnings" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please fix the errors above before deploying." -ForegroundColor Red
    Write-Host ""
    Write-Host "Documentation:" -ForegroundColor Cyan
    Write-Host "  - Setup guide: START_HERE_GCP.md" -ForegroundColor White
    Write-Host "  - Full guide: DEPLOY_GCP.md" -ForegroundColor White
    Write-Host ""
    exit 1
}
