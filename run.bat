@echo off
echo ==============================================
echo GENERADOR DE VIDEOS (SPRITE COMPOSITING)
echo ==============================================
echo.
echo [*] Procesando guion y generando animacion...
echo.

cd /d "%~dp0"
call animator_env\Scripts\python.exe compositor.py

if %errorlevel% neq 0 (
    echo [!] Hubo un error al generar los videos.
    pause
    exit /b %errorlevel%
)

echo.
echo [+] Proceso completado exitosamente. 
echo [+] Revisa el archivo 'video_completo.mp4'
echo.
pause
