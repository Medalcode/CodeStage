@echo off
title AI Video Studio — LTX AI Avatar Engine Launcher
cls
echo ===================================================
echo   Iniciando AI Video Studio (LTX AI Avatar Engine)
echo   Rama Activa: feature/ltx-ai-avatar-engine
echo ===================================================
echo.
echo [*] Configurando Puerto Independiente: 5004
echo [*] Modo de Renderizado: LTX AI Avatar Diffusion Engine (Ghibli Talking Avatar)
echo.
echo [*] Abriendo Dashboard Web en http://localhost:5004...
set PORT=5004
start "" http://localhost:5004
python server.py
pause
