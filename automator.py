import os
import subprocess
import time
import sys
from pathlib import Path

from utils import split_script, generate_audio, ensure_dir, DEFAULT_VOICE

# ==========================================
# CONFIGURACIÓN
# ==========================================
# Las rutas asumen ejecución desde la carpeta SadTalker o raíz
GUION_FILE = "../guion.txt" if os.path.exists("../guion.txt") else "guion.txt"
IMAGE_FILE = "../avatar.png" if os.path.exists("../avatar.png") else "avatar.png"
OUTPUT_DIR = "../resultados_finales" if os.path.exists("../guion.txt") else "resultados_finales"
VOICE = DEFAULT_VOICE

def run_sadtalker(audio_path, image_path, index, output_dir):
    """Ejecuta la inferencia de SadTalker por consola."""
    print(f"[*] Procesando video {index} con SadTalker...")
    
    abs_audio = str(Path(audio_path).resolve())
    abs_image = str(Path(image_path).resolve())
    abs_out = str(Path(output_dir).resolve())

    if not Path(abs_image).exists():
        raise FileNotFoundError(f"No se encontró la imagen de avatar en: {abs_image}")

    cmd = [
        sys.executable, "inference.py",
        "--driven_audio", abs_audio,
        "--source_image", abs_image,
        "--result_dir", abs_out,
        "--preprocess", "full",
        "--enhancer", "gfpgan"
    ]
    
    subprocess.run(cmd, check=True)

def main():
    ensure_dir(OUTPUT_DIR)
    
    try:
        chunks = split_script(GUION_FILE)
    except Exception as e:
        print(f"[!] Error crítico cargando guion: {e}")
        return
        
    print(f"[*] Se encontraron {len(chunks)} bloques de texto para procesar.")
    start_time = time.time()
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n" + "="*40)
        print(f"--- PROCESANDO BLOQUE {i}/{len(chunks)} ---")
        print(f"Texto: {chunk[:50]}...")
        print("="*40)
        
        try:
            audio_path = os.path.join(OUTPUT_DIR, f"audio_{i:03d}.wav")
            generate_audio(chunk, audio_path, voice=VOICE)
            run_sadtalker(audio_path, IMAGE_FILE, i, OUTPUT_DIR)
            
        except subprocess.CalledProcessError as e:
            print(f"[!] Error ejecutando comando en el bloque {i}: {e}")
        except Exception as e:
            print(f"[!] Error inesperado en el bloque {i}: {e}")
            
    elapsed = time.time() - start_time
    print(f"\n[*] Proceso por lotes finalizado en {elapsed/60:.2f} minutos.")
    print(f"[*] Revisa la carpeta '{OUTPUT_DIR}' para ver los resultados.")

if __name__ == "__main__":
    main()
