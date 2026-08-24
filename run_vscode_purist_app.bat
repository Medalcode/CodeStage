@echo off
title AI Video Studio — VS Code Purist IDE Engine Launcher
cls
echo ===================================================
echo   Iniciando AI Video Studio (VS Code Purist Engine)
echo   Rama Activa: feature/vscode-ide-purist-engine
echo ===================================================
echo.
echo [*] Configurando Puerto Independiente: 5003
echo [*] Modo de Renderizado: VS Code IDE Simulator Purista a Pantalla Completa
echo.
echo [*] Abriendo Dashboard Web en http://localhost:5003...
set PORT=5003
start "" http://localhost:5003
python server.py
pause
