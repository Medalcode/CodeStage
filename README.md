# 🎬 AI Video Studio (Automated Technical Tutorial Video Engine) — v2.0

![CI Pipeline](https://github.com/Medalcode/canal-tutorial-automation/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.14-blue.svg)
![Node Version](https://img.shields.io/badge/node->=18.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**AI Video Studio** es un sistema empresarial de automatización de video impulsado por **FastAPI**, **Remotion (React 18 + TypeScript)** y **Edge-TTS**. Permite transformar prompts e ideas técnicas en videos tutoriales dinámicos de alta definición (1080p 30fps) con locución en español sincronizada y edición en vivo mediante Monaco Editor (VS Code Engine).

---

## ✨ Características Principales

* 🚀 **Motor Declarativo Remotion React v4**: Escenas visuales programadas en React con animación a 30 FPS.
* 🎙️ **Locución Sintética Multilingüe (TTS)**: Síntesis de voz neural con caching inteligente por Hash MD5.
* ⏱️ **Duración Dinámica Adaptativa**: Cálculo de fotogramas (`durationInFrames`) basado en la longitud física del audio MP3 generado (videos de 1 a 6 minutos reales).
* 🤖 **Generador Multidominio por IA**: Detección automática de tecnologías (Python Data, Docker DevOps, React, SQL, Git, Linux) generando código y terminales reales.
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

# 4. Iniciar la aplicación completa (Backend + Web GUI)
python server.py
# O en Windows:
# run_app.bat
```

Abre tu navegador en **`http://localhost:5000`** para acceder al estudio interactivo, o visita **`http://localhost:5000/docs`** para explorar la documentación interactiva Swagger / OpenAPI.

---

## ⚙️ Variables de Entorno (`.env`)

Crea un archivo `.env` basado en `.env.example`:

```env
PORT=5000
GEMINI_API_KEY=tu_api_key_de_gemini_opcional
```

> **Nota**: Si no se proporciona `GEMINI_API_KEY`, el sistema utilizará automáticamente el **Motor Multidominio Local** para construir guiones e historias completas.

---

## 🧪 Ejecución de la Suite de Pruebas (`pytest`)

```bash
# Ejecutar todas las 32 pruebas automatizadas
python -m pytest -v
```

---

## 🐳 Despliegue con Docker Compose

```bash
docker-compose up --build
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
