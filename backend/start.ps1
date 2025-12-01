# Script PowerShell para iniciar o servidor
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO SERVIDOR FLASK" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Muda para o diretório do script
Set-Location $PSScriptRoot

# Define qual Python usar
$pythonPath = $null
$pythonFound = $false

# Tenta encontrar Python do sistema primeiro
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonPath = "python"
        Write-Host "[OK] Usando Python do sistema: $pythonVersion" -ForegroundColor Green
        $pythonFound = $true
    }
}
catch {
    # Python do sistema não encontrado
}

# Se não encontrou Python do sistema, tenta venv
if (-not $pythonFound) {
    if (Test-Path "venv\Scripts\python.exe") {
        $pythonPath = "venv\Scripts\python.exe"
        Write-Host "[OK] Usando: venv\Scripts\python.exe" -ForegroundColor Green
        $pythonFound = $true
    }
    elseif (Test-Path "venv\bin\python.exe") {
        $pythonPath = "venv\bin\python.exe"
        Write-Host "[OK] Usando: venv\bin\python.exe" -ForegroundColor Green
        $pythonFound = $true
    }
}

if (-not $pythonFound) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUÇÃO:" -ForegroundColor Yellow
    Write-Host "1. Instale Python do site oficial: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "2. Ou recrie o ambiente virtual:" -ForegroundColor Cyan
    Write-Host "   python -m venv venv" -ForegroundColor White
    Write-Host "   venv\Scripts\activate" -ForegroundColor White
    Write-Host "   pip install -r requirements.txt" -ForegroundColor White
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando servidor..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Executa o app.py e captura a saída
try {
    & $pythonPath app.py
}
catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERRO ao executar servidor!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Erro: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente executar manualmente:" -ForegroundColor Yellow
    Write-Host "  $pythonPath app.py" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Se chegou aqui, o servidor parou
Write-Host ""
Write-Host "Servidor parou." -ForegroundColor Yellow
Read-Host "Pressione Enter para sair"

