# 🎬 AI Video Studio (Automated Technical Tutorial Video Engine) — v2.0

![CI Pipeline](https://github.com/Medalcode/canal-tutorial-automation/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.14-blue.svg)
![Node Version](https://img.shields.io/badge/node->=18.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**AI Video Studio** es un sistema empresarial de automatización de video impulsado por **FastAPI**, **Remotion (React 18 + TypeScript)**, **MoviePy**, **Manim** y **Edge-TTS**. Permite transformar prompts e ideas técnicas en videos tutoriales dinámicos de alta definición (1080p 30fps) con locución en español sincronizada y edición en vivo mediante Monaco Editor (VS Code Engine).

---

## 🏛️ Matriz de Ramas, Motores y Puertos Independientes

El repositorio soporta 5 motores de generación de video organizados en ramas independientes de Git:

| Rama de Git | Motor de Video | Puerto | Lanzador `.bat` | Descripción / Estética |
| :--- | :--- | :--- | :--- | :--- |
| **`main`** | Remotion React 18 | **`5000`** | [`run_app.bat`](file:///c:/Users/Jonatthan/Documents/Github/canal-tutorial-automation/run_app.bat) | Componentes Web React (Navegador SSL, Excel, Power BI, Explorador). |
| **`feature/python-sprite-compositor`** | MoviePy + PIL | **`5001`** | [`run_python_compositor_app.bat`](file:///c:/Users/Jonatthan/Documents/Github/canal-tutorial-automation/run_python_compositor_app.bat) | Pantalla dividida 40/60 con Avatar 2D animado (*Ghibli Programmer*) y Canvas. |
| **`feature/manim-vector-engine`** | Manim Library | **`5002`** | `run_manim_app.bat` | Animaciones vectoriales matemáticas y código estilizado (*3Blue1Brown* style). |
| **`feature/vscode-ide-purist-engine`** | VS Code Simulator | **`5003`** | `run_vscode_purist_app.bat` | Editor VS Code a pantalla completa con tipeo en vivo por IA sin avatar. |
| **`feature/ltx-ai-avatar-engine`** | LTX Diffusion Avatar | **`5004`** | `run_ltx_avatar_app.bat` | Avatar parlante generado por difusor IA / LTX-Video. |

---

## ✨ Características Principales

* 🚀 **Motor Declarativo Remotion React v4**: Escenas visuales programadas en React con animación a 30 FPS.
* 🐍 **Motor Nativo en Python (MoviePy + PIL)**: Composición 40/60 sin dependencias de navegadores web.
* 📐 **Motor Vectorial Manim**: Diagramas y fórmulas matemáticas animadas cuadro a cuadro.
* 🎙️ **Locución Sintética Multilingüe (TTS)**: Síntesis de voz neural con caching inteligente.
* ⏱️ **Duración Dinámica Adaptativa**: Cálculo de fotogramas (`durationInFrames`) basado en la longitud del audio MP3 generado.
* 🤖 **Generador Multidominio por IA**: Detección automática de tecnologías (Python Data, Docker DevOps, React, SQL, Git, Linux).
* ⚡ **FastAPI & WebSockets Telemetry**: Difusión bidireccional cuadro a cuadro en la interfaz web sin polling HTTP.
* 💻 **Monaco Code Editor en Vivo**: Edición de código en tiempo real con VS Code Engine integrado en la web.
* 📺 **Soporte Multi-Formato**: Exportación en formato YouTube (16:9 1080p) y Shorts / TikTok / Reels (9:16 Vertical).
* 💾 **Persistencia SQLite WAL**: Almacenamiento local de proyectos e historial en `studio.db`.

---

## 🛠️ Requisitos Previos

1. **Python 3.10+** (Probado en Python 3.10, 3.11 y 3.14).
2. **Node.js v18.0+** y **npm v9+**.
3. **FFmpeg** instalado en el PATH del sistema (`ffmpeg` y `ffprobe`).

---

## 🚀 Instalación y Arranque Rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/Medalcode/canal-tutorial-automation.git
cd canal-tutorial-automation

# 2. Instalar dependencias de Python
pip install -r requirements.txt

# 3. Instalar dependencias de Remotion (React)
cd remotion-app
npm install
cd ..

# 4. Iniciar la aplicación en cualquiera de los puertos:
# Para la rama activa actual:
python server.py

# O usando el lanzador ejecutable de tu preferencia:
run_app.bat                       # Puerto 5000 (Remotion React)
run_python_compositor_app.bat      # Puerto 5001 (Python 40/60 Sprite)
```

---

## 🧪 Ejecución de Pruebas Automatizadas

```bash
# Ejecutar la suite completa de 34 pruebas unitarias, de integración y smoke:
python -m pytest -v
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**.
