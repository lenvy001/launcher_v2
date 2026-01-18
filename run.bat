@echo off
REM Script para executar o Launcher V2

echo ========================================
echo   LAUNCHER V2 - App Manager
echo ========================================
echo.
echo [1] Web Interface (Flask - localhost:5000)
echo [2] CLI Menu
echo [0] Exit
echo.
set /p choice="Choose: "

if "%choice%"=="1" (
    echo.
    echo Starting Flask server...
    cd src
    python serve.py
) else if "%choice%"=="2" (
    echo.
    echo Starting CLI Menu...
    cd src
    python main.py
) else if "%choice%"=="0" (
    exit /b 0
) else (
    echo Invalid choice
    exit /b 1
)
