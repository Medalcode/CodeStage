# Canal Tutorial Automation

[![CI Pipeline](https://github.com/Medalcode/canal-tutorial-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/Medalcode/canal-tutorial-automation/actions/workflows/ci.yml)

Sistema automatizado en Python para generar videos de YouTube con un avatar parlante animado. Toma un guion en formato de texto (`guion.txt`) y produce un video completo con sincronización labial, parpadeo, movimiento de ojos y animación de manos, todo renderizado localmente sin necesidad de suscripciones de pago.

---

## 🚀 Modos de funcionamiento

El proyecto soporta dos pipelines de generación según el hardware disponible:

### Modo A — Sprite Compositing (Python puro / Recomendado)
Ideal para cualquier PC (funciona en CPU sin necesidad de GPU dedicada). Utiliza imágenes PNG como capas (sprites) compuestas cuadro a cuadro mediante `Pillow`, `MoviePy` y `Rhubarb Lip Sync`.

### Modo B — SadTalker (IA con GPU)
Genera animación fotorrealista a partir de una única imagen de personaje (`avatar.png`) usando el modelo de Deep Learning **SadTalker**. Requiere una GPU NVIDIA con soporte CUDA (probado en RTX 4060).

---

## 🛠️ Flujo de trabajo (Modo Sprite Compositing)

1. **Texto a Voz (TTS)**: `edge-tts` convierte cada párrafo de `guion.txt` a audio (`.mp3` y `.wav`).
2. **Lip Sync (Visemas)**: `Rhubarb Lip Sync` analiza el audio en WAV y genera una secuencia de visemas en un archivo JSON (`mouthCues`).
3. **Composición frame a frame**: `compositor.py` apila dinámicamente las capas del avatar usando `Pillow`:
   - **Boca**: Animada en tiempo real según el visema actual (A, B, C, D, E, F, X).
   - **Ojos**: Parpadeo aleatorio/periódico y alternancia de mirada (frente / pantalla).
   - **Manos**: Animación de tipear al mirar la pantalla y posición de reposo al mirar a la cámara.
   - **Cuerpo**: Efecto sutil de respiración.
   - **Pelo**: Capa superior para dar profundidad visual.
4. **Renderizado de clips**: `MoviePy` ensambla las imágenes compuestas y el audio en clips de video por cada párrafo.
5. **Ensamblaje final**: `unir_videos.py` concatena secuencialmente los clips resultantes en `video_completo.mp4` mediante FFmpeg.

---

## 📂 Estructura del proyecto

```
canal-tutorial-automation/
├── .github/workflows/ci.yml       # Pipeline de CI en GitHub Actions
├── tests/                          # Suite de pruebas automatizadas (Unit, Integration, Smoke)
├── utils.py                        # Módulo central de utilidades (TTS, guion, paths)
├── pyproject.toml                  # Configuración estándar del paquete Python
├── requirements.txt                # Dependencias declarativas del proyecto
├── CHANGELOG.md                    # Historial de cambios siguiendo Keep a Changelog
├── .env.example                    # Plantilla de variables de entorno
├── run.bat                         # Punto de entrada principal (Sprite Compositing)
├── compositor.py                   # Renderizador del avatar 2D por capas (Sprite Compositing)
├── automator.py                    # Orquestador del pipeline SadTalker
├── unir_videos.py                  # Concatena clips con FFmpeg usando duraciones exactas
├── download_rhubarb.py             # Script para descargar automáticamente Rhubarb Lip Sync
├── preparar_personaje.py           # Generador automático de assets 2D base/placeholder
├── generate_placeholder_assets.py  # Generador alternativo de placeholders vectoriales/dibujados
├── prepare_assets.py               # Herramienta auxiliar de procesamiento de imágenes
├── download_models_script.py       # Descarga modelos preentrenados de SadTalker y GFPGAN
├── install_windows.ps1             # Instalador automático para Windows (SadTalker)
├── guion.txt                       # Guion a leer (párrafos separados por línea en blanco)
├── Dockerfile                      # Imagen Docker con soporte CUDA para SadTalker
├── docker-compose.yml              # Configuración de Docker Compose con GPU NVIDIA
├── assets/                         # Sprites PNG transparentes del avatar
│   ├── body.png                    # Cuerpo del avatar
│   ├── hair.png                    # Cabello (capa superior)
│   ├── mouth/                      # Sprites de boca (mouth_X.png, mouth_A.png ... mouth_F.png)
│   ├── eyes/                       # Sprites de ojos (eyes_forward.png, eyes_screen.png, eyes_blink.png)
│   └── hands/                      # Sprites de manos (hands_type_1.png ... hands_type_3.png)
├── rhubarb/                        # Carpeta del ejecutable de Rhubarb Lip Sync
└── resultados_finales/             # Audios y clips intermedios generados
```

---

## 📋 Requisitos

### Modo Sprite Compositing
- **Python 3.10+**
- Dependencias de Python: `moviepy`, `Pillow`, `numpy`, `edge-tts`
- **Rhubarb Lip Sync** (se puede descargar automáticamente con `python download_rhubarb.py`)
- **FFmpeg** instalado y disponible en el PATH del sistema

### Modo SadTalker (Windows nativo)
- **Python 3.10**
- GPU NVIDIA con CUDA 12.1 (recomendado RTX 4060 o superior)
- Git / Git Bash

### Modo SadTalker (Docker)
- Docker Desktop con integración WSL2
- NVIDIA Container Toolkit

---

## ⚡ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/Medalcode/canal-tutorial-automation.git
cd canal-tutorial-automation
```

### 2. Configurar Sprite Compositing (CPU)

```powershell
# Crear entorno virtual e instalar dependencias
python -m venv animator_env
.\animator_env\Scripts\Activate.ps1
pip install -r requirements.txt

# Descargar Rhubarb Lip Sync automáticamente
python download_rhubarb.py

# Generar assets de personaje base (si no posees imágenes personalizadas)
python preparar_personaje.py
```

### 3. Configurar SadTalker (GPU - Opcional)

#### Opción A: Windows Nativo
```powershell
.\install_windows.ps1
```

#### Opción B: Docker
```bash
docker compose up -d --build
docker exec -it sadtalker-env bash
```

---

## 🧪 Pruebas Automatizadas

El proyecto incluye una suite de pruebas automatizadas con `pytest`:

```bash
# Ejecutar todas las pruebas unitarias y de integración
python -m pytest -v
```

---

## 🎮 Modo de Uso

### Generar Video con Sprite Compositing

1. Edita el archivo `guion.txt` escribiendo el texto del tutorial. Separa los párrafos con una línea en blanco.
2. Asegúrate de tener los sprites en la carpeta `assets/` (o genera los por defecto con `python preparar_personaje.py`).
3. Ejecuta el renderizador:
   ```powershell
   python compositor.py
   ```
   o haz doble clic en `run.bat`.
4. El video resultante se guardará en la raíz como `video_completo.mp4`.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
