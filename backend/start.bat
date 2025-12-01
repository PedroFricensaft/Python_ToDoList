@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   INICIANDO SERVIDOR FLASK
echo ========================================
echo.

REM Tenta ativar o venv e usar python
if exist "venv\Scripts\activate.bat" (
    echo [OK] Ativando ambiente virtual (Windows)...
    call venv\Scripts\activate.bat
    python app.py
    goto :end
)

if exist "venv\bin\activate" (
    echo [OK] Ativando ambiente virtual (Linux/Mac)...
    call venv\bin\activate
    python app.py
    goto :end
)

REM Tenta executar Python diretamente
if exist "venv\Scripts\python.exe" (
    echo [OK] Executando: venv\Scripts\python.exe
    venv\Scripts\python.exe app.py
    goto :end
)

if exist "venv\bin\python.exe" (
    echo [OK] Executando: venv\bin\python.exe
    venv\bin\python.exe app.py
    goto :end
)

REM Última tentativa: Python do sistema
echo [AVISO] Tentando Python do sistema...
python app.py
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERRO: Python nao encontrado!
    echo ========================================
    echo.
    echo SOLUCAO: Execute no PowerShell:
    echo.
    echo   cd backend
    echo   .\venv\bin\python app.py
    echo.
    pause
    exit /b 1
)

:end
if errorlevel 1 (
    echo.
    echo Servidor parou com erro.
    pause
)

