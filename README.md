# Canal Tutorial Automation

Este proyecto es un sistema automatizado para generar videos para un canal de YouTube. El objetivo principal es tomar un guion de texto y generar un video con un avatar animado que habla y se mueve, con su respectivo audio sincronizado.

## Arquitectura (Sprite Compositing)

El sistema actual utiliza una técnica de "Sprite Compositing" en Python puro. 

### Flujo de trabajo:
1. **Texto a Voz (TTS):** Se utiliza `edge-tts` para convertir el texto del archivo `guion.txt` a un archivo de audio (.mp3 y luego a .wav).
2. **Sincronización Labial (Lip Sync):** El audio .wav es procesado por `Rhubarb Lip Sync` para generar un archivo JSON con los visemas (formas de la boca) y sus tiempos correspondientes.
3. **Composición de Video:** El script `compositor.py` lee el audio, el JSON de visemas y una serie de imágenes (sprites) de la carpeta `assets/`.
4. **Renderizado:** Usando `MoviePy` y `Pillow`, se compone frame a frame el video final, animando:
   - Movimiento de labios (Lip Sync).
   - Parpadeo de ojos.
   - Cambio de mirada (hacia la pantalla y hacia la cámara).
   - Movimiento de las manos (tipeando).
   - Respiración (movimiento sutil del cuerpo).
5. **Ensamblaje:** Los clips generados por cada párrafo del guion se unen en un solo archivo `video_completo.mp4`.

## Estructura de Archivos

- `run.bat`: Archivo ejecutable principal. Haz doble clic para iniciar todo el proceso.
- `compositor.py`: El script principal en Python que orquesta la generación de audio, visemas y renderizado del video.
- `guion.txt`: Archivo de texto donde debes colocar el guion que leerá el avatar. Separa los párrafos con una línea en blanco.
- `assets/`: Carpeta que contiene las partes del cuerpo del avatar (cuerpo, pelo, manos, ojos y bocas). **(Debes reemplazar los placeholders con tus propias imágenes PNG transparentes).**
- `rhubarb/`: Contiene el ejecutable de Rhubarb Lip Sync.
- `animator_env/`: Entorno virtual de Python con las dependencias necesarias instaladas (`moviepy`, `Pillow`, `numpy`, `edge-tts`).

## Cómo usar

1. Escribe tu guion en `guion.txt`.
2. Asegúrate de tener tus imágenes PNG con fondo transparente en la carpeta `assets/` respetando los nombres de archivo.
3. Ejecuta `run.bat`.
4. El video final se generará en la raíz del proyecto como `video_completo.mp4`.
