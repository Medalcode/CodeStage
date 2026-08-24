@echo off
title AI Video Studio — Manim Vector Engine Launcher
cls
echo ===================================================
echo   Iniciando AI Video Studio (Manim Vector Engine)
echo   Rama Activa: feature/manim-vector-engine
echo ===================================================
echo.
echo [*] Configurando Puerto Independiente: 5002
echo [*] Modo de Renderizado: Manim Vector Animations (Estilo 3Blue1Brown)
echo.
echo [*] Abriendo Dashboard Web en http://localhost:5002...
set PORT=5002
start "" http://localhost:5002
python server.py
pause
