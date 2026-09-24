@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Agent Cripto TDR

if not exist ".install_ok" goto :install
if not exist ".venv\Scripts\python.exe" goto :install

".venv\Scripts\python.exe" -c "import streamlit, pandas, numpy, plotly, ccxt" >nul 2>nul
if errorlevel 1 goto :install

echo Iniciant Agent Cripto TDR...
start "" /B powershell.exe -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8501'" >nul 2>nul
".venv\Scripts\python.exe" -m streamlit run "app\app.py" --server.headless true --browser.gatherUsageStats false --server.address localhost --server.port 8501
exit /b %errorlevel%

:install
echo L'aplicacio no esta preparada o falta alguna dependencia.
echo Executant la preparacio automatica...
call "%~dp0INSTAL_LAR_AGENT.bat"
exit /b %errorlevel%
