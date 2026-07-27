# Canal Tutorial Automation

Sistema automatizado para generar videos de YouTube con un avatar parlante animado. Toma un guion de texto y produce un video con sincronización labial, parpadeo, movimiento de ojos y animación de manos, todo renderizado localmente sin suscripciones de pago.

---

## Modos de funcionamiento

El proyecto soporta dos pipelines según el hardware disponible:

### Modo A — Sprite Compositing (Python puro)
Ideal para cualquier PC sin necesidad de GPU potente. Usa imágenes PNG como sprites para componer el avatar frame a frame.

### Modo B — SadTalker (IA con GPU)
Genera un video realista a partir de una foto (`avatar.png`) usando el modelo SadTalker. Requiere una GPU NVIDIA con soporte CUDA (probado en RTX 4060).

---

## Flujo de trabajo (Modo Sprite Compositing)

1. **Texto a Voz** — `edge-tts` convierte cada párrafo de `guion.txt` a audio `.mp3` / `.wav`.
2. **Lip Sync** — `Rhubarb Lip Sync` analiza el audio y genera un JSON con los visemas y sus tiempos.
3. **Composición frame a frame** — `compositor.py` apila las capas del avatar usando `Pillow`:
   - Boca animada con los visemas del JSON
   - Parpadeo de ojos aleatorio
   - Cambio de mirada (pantalla / cámara)
   - Manos tipeando
   - Respiración sutil del cuerpo
4. **Renderizado** — `MoviePy` ensambla los frames y el audio en un clip por párrafo.
5. **Ensamblaje final** — `unir_videos.py` concatena todos los clips en `video_completo.mp4` vía FFmpeg.

---

## Flujo de trabajo (Modo SadTalker)

1. **Texto a Voz** — `automator.py` genera el audio con `edge-tts`.
2. **Inferencia IA** — `SadTalker` (`inference.py`) toma el audio y `avatar.png` y produce un video realista con sincronización labial y movimiento facial.
3. **Ensamblaje final** — `unir_videos.py` une los clips generados en `video_completo.mp4`.

---

## Estructura del proyecto

```
canal-tutorial-automation/
├── run.bat                    # Punto de entrada principal (Sprite Compositing)
├── compositor.py              # Renderizador del avatar (Sprite Compositing)
├── automator.py               # Orquestador del pipeline SadTalker
├── unir_videos.py             # Concatena clips con FFmpeg
├── download_models_script.py  # Descarga modelos de SadTalker y GFPGAN
├── install_windows.ps1        # Instalador automático para Windows (SadTalker)
├── guion.txt                  # Guion a leer (párrafos separados por línea en blanco)
├── avatar.png                 # Foto del personaje (modo SadTalker)
├── Dockerfile                 # Imagen Docker con CUDA para SadTalker
├── docker-compose.yml         # Compose con soporte GPU NVIDIA
├── assets/
│   ├── body.png               # Cuerpo del avatar (PNG transparente)
│   ├── hair.png               # Pelo del avatar (PNG transparente)
│   ├── mouth/                 # Sprites de boca (mouth_X/A/B/C/D/E/F.png)
│   ├── eyes/                  # Sprites de ojos (forward / screen / blink)
│   └── hands/                 # Sprites de manos (type_1/2/3.png)
├── rhubarb/                   # Ejecutable de Rhubarb Lip Sync
└── resultados_finales/        # Audios y clips generados
```

---

## Requisitos

### Modo Sprite Compositing
- Python 3.10+
- Entorno virtual `animator_env` con: `moviepy`, `Pillow`, `numpy`, `edge-tts`
- [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) (incluido en `rhubarb/`)
- FFmpeg en el PATH

### Modo SadTalker (Windows nativo)
- Python 3.10
- GPU NVIDIA con CUDA 12.1 (recomendado RTX 4060 o superior)
- Git y, opcionalmente, Git Bash (para el script de descarga de modelos)

### Modo SadTalker (Docker)
- Docker Desktop con soporte WSL2
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

---

## Instalación

### Sprite Compositing
```powershell
# Crear entorno virtual e instalar dependencias
python -m venv animator_env
.\animator_env\Scripts\Activate.ps1
pip install moviepy pillow numpy edge-tts
```

### SadTalker — Windows nativo
```powershell
# Ejecutar el instalador automático desde la raíz del proyecto
.\install_windows.ps1
```
El script clona SadTalker, crea el entorno virtual `sadtalker_env`, instala PyTorch con CUDA 12.1, aplica el parche de `basicsr` y descarga los modelos preentrenados.

### SadTalker — Docker
```bash
docker compose up -d --build
docker exec -it sadtalker-env bash
```

---

## Cómo usar

### Sprite Compositing
1. Escribe tu guion en `guion.txt` (párrafos separados por una línea en blanco).
2. Coloca tus imágenes PNG con fondo transparente en `assets/` respetando los nombres de archivo.
3. Ejecuta `run.bat` o directamente:
   ```powershell
   .\animator_env\Scripts\python.exe compositor.py
   ```
4. El video final se genera como `video_completo.mp4` en la raíz.

### SadTalker
1. Escribe tu guion en `guion.txt`.
2. Coloca la foto del personaje en `avatar.png`.
3. Activa el entorno y ejecuta el automator desde dentro de la carpeta `SadTalker/`:
   ```powershell
   .\sadtalker_env\Scripts\Activate.ps1
   cd SadTalker
   python ..\automator.py
   ```
4. Una vez generados los clips en `resultados_finales/`, únelos:
   ```powershell
   python unir_videos.py
   ```

---

## Voces disponibles (edge-tts)

La voz se configura en `automator.py` o `compositor.py` mediante la variable `VOICE`. Algunas opciones en español:

| Voz | Variante |
|-----|----------|
| `es-MX-DaliaNeural` | Español México (femenino) |
| `es-MX-JorgeNeural` | Español México (masculino) |
| `es-ES-ElviraNeural` | Español España (femenino) |
| `es-ES-AlvaroNeural` | Español España (masculino) |

Para listar todas las voces disponibles:
```bash
edge-tts --list-voices
```

---

## Assets del avatar

Los sprites deben ser archivos PNG con fondo transparente ubicados en `assets/`:

| Archivo | Descripción |
|---------|-------------|
| `body.png` | Cuerpo completo del personaje |
| `hair.png` | Cabello (capa superior) |
| `mouth/mouth_X.png` | Boca cerrada (silencio) |
| `mouth/mouth_A.png` — `mouth_F.png` | Visemas A–F de Rhubarb |
| `eyes/eyes_forward.png` | Ojos mirando al frente |
| `eyes/eyes_screen.png` | Ojos mirando a la pantalla |
| `eyes/eyes_blink.png` | Ojos cerrados (parpadeo) |
| `hands/hands_type_1.png` — `hands_type_3.png` | Animación de teclado |

---

## Licencia

MIT
