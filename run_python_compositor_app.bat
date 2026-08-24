@echo off
title AI Video Studio — Python Native 40/60 Compositor Launcher
cls
echo ===================================================
echo   Iniciando AI Video Studio (Python 40/60 Engine)
echo   Rama Activa: feature/python-sprite-compositor
echo ===================================================
echo.
echo [*] Configurando Puerto Independiente: 5001
echo [*] Modo de Renderizado: Python Nativo (MoviePy + PIL + FFmpeg + Avatar 2D)
echo [*] Sin dependencias de Node.js ni Remotion.
echo.
echo [*] Abriendo Dashboard Web en http://localhost:5001...
set PORT=5001
start "" http://localhost:5001
python server.py
pause
