# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-08-11

### ✨ Añadido (Feat)
- **Motor de Renderizado Remotion React (v4.0)**: Migración de motor gráfico a componentes declarativos en React 18 a 30 FPS en resolución 1080p.
- **Servidor FastAPI & Telemetría por WebSockets**: Backend con endpoints REST `/api/generate-script`, `/api/render-video`, `/api/projects` y `/ws/render` para avance cuadro a cuadro.
- **Interfaz Web Studio GUI con Monaco Editor**: Panel web responsive en Vanilla JS con Monaco Editor (VS Code Engine) integrado para edición en vivo de código.
- **Duración Dinámica de Video por Medición de Audio**: Medición real en segundos de archivos de audio sintetizados por `edge-tts` ajustando los fotogramas de cada escena (`durationInFrames`).
- **Generador de Guiones Multidominio por IA (`generator/script_generator.py`)**: Detección automática de tecnologías (Python, Pandas, Docker, React, SQL, Git) generando ejemplos reales sin plantillas estáticas repetitivas.
- **Persistencia en SQLite (`database.py`)**: Base de datos SQLite `studio.db` con modo WAL (Write-Ahead Logging) habilitado.
- **Soporte para Formatos 16:9 y 9:16 Shorts**: Composiciones `ExpressApiVideo` y `ExpressApiVideoShorts`.

### ⚡ Cambiado (Refactor)
- Desacoplamiento del generador de guiones desde `server.py` hacia el paquete modular `generator/script_generator.py` aplicando el Principio de Responsabilidad Única (SRP).
- Subprocesos de renderizado en Windows ejecutados mediante `cmd.exe /c npx remotion render` evitando bloqueos de consola.

### 🧪 Pruebas & Calidad (Test)
- Cobertura expandida a **32 pruebas pasadas (100%)** abarcando endpoints API, generador multidominio, persistencia SQLite y regresión visual de fotogramas.

---

## [1.1.0] - 2026-08-04

### Añadido
- Módulo centralizado `utils.py` para parseo de guiones multi-encoding (`split_script`), generación de audio TTS (`generate_audio`) y resolución multiplataforma de ejecutables binarios (`get_rhubarb_path`).
- Suite de pruebas automatizadas con `pytest` en el directorio `tests/` con 17 pruebas unitarias, de integración y smoke E2E.
- Pipeline de Integración Continua (CI) con GitHub Actions en `.github/workflows/ci.yml`.

---

## [1.0.0] - 2026-08-01

### Añadido
- Versión inicial con soporte para Sprite Compositing 2D (`compositor.py`) e inferencia con SadTalker (`automator.py`).
