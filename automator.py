import os
import subprocess
import time
import sys
import time

# ==========================================
# CONFIGURACIÓN
# ==========================================
# Las rutas asumen que este script se ejecuta dentro de la carpeta SadTalker
GUION_FILE = "../guion.txt"           # Tu archivo de texto con el guion (arriba un nivel)
IMAGE_FILE = "../avatar.png"          # La imagen de tu personaje (arriba un nivel)
OUTPUT_DIR = "../resultados_finales"  # Carpeta donde se guardará todo (arriba un nivel)

# Voz de Microsoft Edge TTS (Ejemplo: voz femenina de México, también puede ser es-ES-ElviraNeural)
VOICE = "es-MX-DaliaNeural"

def split_script(file_path):
    """Divide el guion en bloques basados en dobles saltos de línea."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Separar por párrafos y limpiar espacios en blanco
    chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
    return chunks

def generate_audio(text, index):
    """Genera el archivo de audio usando edge-tts."""
    audio_filename = f"audio_{index:03d}.wav"
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)
    
    print(f"[*] Generando audio {index}...")
    cmd = [
        "edge-tts", 
        "--text", text, 
        "--voice", VOICE, 
        "--write-media", audio_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return audio_path

def run_sadtalker(audio_path, image_path, index):
    """Ejecuta la inferencia de SadTalker por consola."""
    print(f"[*] Procesando video {index} con SadTalker en la RTX 4060...")
    
    # Asegurar rutas absolutas para evitar problemas con SadTalker
    abs_audio = os.path.abspath(audio_path)
    abs_image = os.path.abspath(image_path)
    abs_out = os.path.abspath(OUTPUT_DIR)

    cmd = [
        sys.executable, "inference.py",
        "--driven_audio", abs_audio,
        "--source_image", abs_image,
        "--result_dir", abs_out,
        "--preprocess", "full",
        "--enhancer", "gfpgan"
    ]
    
    # Ejecutamos el comando. Se mostrará el progreso de PyTorch en la consola.
    subprocess.run(cmd, check=True)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        chunks = split_script(GUION_FILE)
    except Exception as e:
        print(f"[!] Error crítico: {e}")
        return
        
    print(f"[*] Se encontraron {len(chunks)} bloques de texto para procesar.")
    start_time = time.time()
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n" + "="*40)
        print(f"--- PROCESANDO BLOQUE {i}/{len(chunks)} ---")
        print(f"Texto: {chunk[:50]}...") # Muestra un extracto del texto
        print("="*40)
        
        try:
            # 1. Generar Audio
            audio_path = generate_audio(chunk, i)
            # 2. Generar Video
            run_sadtalker(audio_path, IMAGE_FILE, i)
            
        except subprocess.CalledProcessError as e:
            print(f"[!] Error ejecutando comando en el bloque {i}: {e}")
        except Exception as e:
            print(f"[!] Error inesperado en el bloque {i}: {e}")
            
    elapsed = time.time() - start_time
    print(f"\n[*] Proceso por lotes finalizado en {elapsed/60:.2f} minutos.")
    print(f"[*] Revisa la carpeta '{OUTPUT_DIR}' para ver los resultados.")

if __name__ == "__main__":
    main()
