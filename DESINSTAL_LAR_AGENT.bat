@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Agent Cripto TDR - Neteja

echo Aquesta opcio elimina l'entorn Python de l'aplicacio i l'acces directe.
echo Les dades i el codi del projecte es conservaran.
echo.
choice /C SN /N /M "Vols continuar? [S/N] "
if errorlevel 2 exit /b 0

if exist ".venv" rmdir /S /Q ".venv"
if exist ".install_ok" del /Q ".install_ok"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$p=Join-Path ([Environment]::GetFolderPath('Desktop')) 'Agent Cripto TDR.lnk'; if(Test-Path $p){Remove-Item $p -Force}" >nul 2>nul

echo.
echo Entorn de l'aplicacio eliminat.
echo El runtime Python compartit de l'Agent es conserva per facilitar una reinstal·lacio.
pause
