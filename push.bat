@echo off
REM Script para fazer push para GitHub
REM Edite: SEU_USUARIO antes de executar

setlocal enabledelayedexpansion

echo ========================================
echo  PUSH PARA GITHUB
echo ========================================
echo.

set /p USUARIO="Digite seu usuario GitHub: "
set REPO=launcher-v2
set URL=https://github.com/!USUARIO!/!REPO!.git

echo.
echo URL: !URL!
echo.
echo [1] Criar repositorio vazio em: https://github.com/new
echo [2] (pressione ENTER quando pronto)
pause

cd "c:\vs code\launcher_v2"

echo.
echo Configurando remoto...
& "C:\Program Files\Git\bin\git.exe" remote add origin !URL!

echo.
echo Renomeando branch para main...
& "C:\Program Files\Git\bin\git.exe" branch -M main

echo.
echo Fazendo push inicial...
& "C:\Program Files\Git\bin\git.exe" push -u origin main

echo.
echo ========================================
echo  CONCLUIDO!
echo  Seu repositorio: !URL!
echo ========================================
pause
