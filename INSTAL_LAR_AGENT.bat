@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Agent Cripto TDR - Instal·lador

echo ======================================================
echo        AGENT CRIPTO TDR - INSTAL·LADOR AUTOMATIC
echo ======================================================
echo.
echo No cal instal·lar Python ni Streamlit manualment.
echo L'instal·lador ho prepara tot de forma automatica.
echo Cal connexio a Internet durant aquesta primera instal·lacio.
echo.

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
if errorlevel 1 goto :error

echo.
choice /C SN /N /M "Vols iniciar l'Agent ara? [S/N] "
if errorlevel 2 exit /b 0
call "%~dp0INICIAR_AGENT.bat"
exit /b 0

:error
echo.
echo S'ha produit un error. Consulta install.log dins la carpeta de l'Agent.
pause
exit /b 1
