# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-04

### Añadido
- Módulo centralizado `utils.py` para parseo de guiones multi-encoding (`split_script`), generación de audio TTS (`generate_audio`) y resolución multiplataforma de ejecutables binarios (`get_rhubarb_path`).
- Suite de pruebas automatizadas con `pytest` en el directorio `tests/` con 17 pruebas unitarias, de integración y smoke E2E.
- Pipeline de Integración Continua (CI) con GitHub Actions en `.github/workflows/ci.yml`.
- Archivos de configuración `.dockerignore`, `.env.example` y `pyproject.toml`.
- Documentos de evaluación de arquitectura, revisión de código PR e informe de testing QA en artefactos.

### Cambiado
- Refactorización de `compositor.py` con liberación explícita de destructores de `MoviePy` (`.close()`) para prevenir fugas de memoria y handles de archivo.
- Refactorización de `preparar_personaje.py` eliminando llamadas dinámicas inline de `pip install`.
- Refactorización de `unir_videos.py` con verificación de FFmpeg y limpieza garantizada de temporales.

### Corregido
- Eliminación de rutas absolutas locales hardcodeadas (`C:\Users\...` y `E:\Github\...`) en `prepare_assets.py`.
- Corrección de descargas multiplataforma en `download_rhubarb.py`.

---

## [1.0.0] - 2026-08-01

### Añadido
- Versión inicial con soporte para Sprite Compositing 2D (`compositor.py`) e inferencia con SadTalker (`automator.py`).
