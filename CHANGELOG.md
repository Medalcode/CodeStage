# 📝 CHANGELOG — AI Video Studio

Todos los cambios notables en este proyecto están documentados en este archivo siguiendo [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).

---

## [2.1.0] — 2026-08-23

### 🚀 Añadido (Added)
- **Matriz de 5 Ramas Independientes**:
  - `main`: Remotion React 18 Engine (Puerto 5000 / `run_app.bat`).
  - `feature/python-sprite-compositor`: Python 40/60 Sprite Compositor (Puerto 5001 / `run_python_compositor_app.bat`).
  - `feature/manim-vector-engine`: Manim Vector Engine (Puerto 5002 / `run_manim_app.bat`).
  - `feature/vscode-ide-purist-engine`: VS Code Purist IDE Simulator (Puerto 5003 / `run_vscode_purist_app.bat`).
  - `feature/ltx-ai-avatar-engine`: LTX AI Avatar Diffusion Engine (Puerto 5004 / `run_ltx_avatar_app.bat`).
- **Nuevos Componentes UI de Remotion (React 18)**: `BrowserWindow.tsx` (Navegador SSL), `ExcelWindow.tsx` (Hoja de cálculo), `FileExplorerWindow.tsx` (Árbol de proyecto), `AnalyticsChartWindow.tsx` (Power BI Dashboard), `ImageShowcaseWindow.tsx` (Galería visual).
- **Habilidades Oficiales Remotion (`remotion-dev/skills`)**: Integración de 12 habilidades de IA para video programático en `.agents/skills/`.

### 🛠️ Cambios y Refactorizaciones (Changed)
- **FastAPI Lifespan API**: Migrado el evento deprecado `@app.on_event("startup")` a administrador de contexto asíncrono `@asynccontextmanager lifespan`.
- **Insignias Dinámicas en Dashboard**: Identificación visual del puerto y motor activo en la cabecera del Dashboard.

### 🧪 Pruebas (Security & Quality)
- Suite ampliada a **34 pruebas automatizadas pasadas en 100% de éxito**.

---

## [2.0.0] — 2026-08-11

### 🚀 Añadido (Added)
- **Motor Remotion React v4**: Renderizado declarativo con resorte `spring` a 30 FPS.
- **FastAPI & WebSockets Telemetry**: Comunicación en tiempo real cuadro a cuadro con el frontend.
- **Generador de Guiones IA Multidominio**: Sincronización automática de código y audios para Python, Docker, React y SQL.

---

## [1.0.0] — 2026-08-04

### 🚀 Añadido (Added)
- Lanzamiento inicial con backend en Python y síntesis de voz Edge-TTS.
