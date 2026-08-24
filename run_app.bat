@echo off
title AI Video Studio Launcher
echo ===================================================
echo   Iniciando AI Video Studio...
echo ===================================================
echo.
echo [*] Configurando Puerto Independiente: 5000
echo [*] Iniciando servidor backend local en http://localhost:5000...
set PORT=5000
start "" http://localhost:5000
python server.py
pause
