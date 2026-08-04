import os
import json
import subprocess
import math
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import VideoClip, AudioFileClip, concatenate_videoclips

from utils import split_script, generate_audio, get_rhubarb_path, ensure_dir, DEFAULT_VOICE

# Configuración
GUION_FILE = "guion.txt"
OUTPUT_DIR = "resultados_finales"
VOICE = DEFAULT_VOICE
FPS = 24

def load_avatar_assets(assets_dir="assets"):
    """Carga y valida todas las capas de imagen PNG para el avatar 2D."""
    base_path = Path(assets_dir)
    if not base_path.exists():
        raise FileNotFoundError(
            f"No se encontró el directorio '{assets_dir}'. "
            "Ejecuta 'python preparar_personaje.py' para generar los assets base."
        )

    try:
        body_img = Image.open(base_path / 'body.png').convert("RGBA")
        hair_img = Image.open(base_path / 'hair.png').convert("RGBA")
        
        eyes_forward = Image.open(base_path / 'eyes' / 'eyes_forward.png').convert("RGBA")
        eyes_screen = Image.open(base_path / 'eyes' / 'eyes_screen.png').convert("RGBA")
        eyes_blink = Image.open(base_path / 'eyes' / 'eyes_blink.png').convert("RGBA")
        
        mouths = {
            shape: Image.open(base_path / 'mouth' / f'mouth_{shape}.png').convert("RGBA") 
            for shape in ['A', 'B', 'C', 'D', 'E', 'F', 'X']
        }
        
        hands = {
            1: Image.open(base_path / 'hands' / 'hands_type_1.png').convert("RGBA"),
            2: Image.open(base_path / 'hands' / 'hands_type_2.png').convert("RGBA"),
            3: Image.open(base_path / 'hands' / 'hands_type_3.png').convert("RGBA"),
        }
        return {
            'body': body_img,
            'hair': hair_img,
            'eyes_forward': eyes_forward,
            'eyes_screen': eyes_screen,
            'eyes_blink': eyes_blink,
            'mouths': mouths,
            'hands': hands
        }
    except Exception as e:
        raise RuntimeError(
            f"Error cargando assets desde '{assets_dir}': {e}. "
            "Asegúrate de ejecutar 'python preparar_personaje.py'."
        ) from e

def run_pipeline():
    ensure_dir(OUTPUT_DIR)
    
    print("[*] Cargando assets de imagen...")
    try:
        assets = load_avatar_assets()
    except Exception as e:
        print(f"[!] {e}")
        return

    body_img = assets['body']
    hair_img = assets['hair']
    eyes_forward = assets['eyes_forward']
    eyes_screen = assets['eyes_screen']
    eyes_blink = assets['eyes_blink']
    mouths = assets['mouths']
    hands = assets['hands']

    rhubarb_exe = get_rhubarb_path()
    if not os.path.exists(rhubarb_exe):
        print(f"[!] No se encontró el ejecutable de Rhubarb Lip Sync en: {rhubarb_exe}")
        print("[!] Ejecuta 'python download_rhubarb.py' para descargarlo automáticamente.")
        return

    chunks = split_script(GUION_FILE)
    clips = []
    
    try:
        for i, text in enumerate(chunks, 1):
            print(f"\n======================================")
            print(f"[*] Procesando bloque {i}/{len(chunks)}...")
            print(f"======================================")
            
            # 1. Generación de Audio
            audio_mp3_path = f"{OUTPUT_DIR}/audio_{i}.mp3"
            audio_path = f"{OUTPUT_DIR}/audio_{i}.wav"
            print("[*] Generando audio TTS...")
            generate_audio(text, audio_mp3_path, voice=VOICE)
            
            # Convertir a WAV (requerido por Rhubarb Lip Sync) usando FFmpeg
            subprocess.run([
                "ffmpeg", "-y", "-i", audio_mp3_path, 
                "-acodec", "pcm_s16le", "-ar", "16000", audio_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 2. Análisis de Lip Sync con Rhubarb
            viseme_path = f"{OUTPUT_DIR}/visemes_{i}.json"
            print("[*] Analizando audio para sincronización labial (visemas)...")
            
            subprocess.run([
                rhubarb_exe, 
                "-f", "json", 
                "-o", viseme_path, 
                audio_path
            ], check=True, stdout=subprocess.DEVNULL)
            
            # Cargar visemas producidos por Rhubarb
            with open(viseme_path, 'r', encoding='utf-8') as f:
                cues = json.load(f).get('mouthCues', [])
                
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            def make_frame(t):
                # Crear frame base transparente
                frame = Image.new("RGBA", body_img.size, (255, 255, 255, 255))
                
                # Efecto de respiración (desplazamiento vertical en Y)
                by = int(math.sin(t * 2 * math.pi / 3.0) * 2)
                
                # Capa 1: Cuerpo
                frame.paste(body_img, (0, by), body_img)
                
                # Capa 2: Ojos (Lógica de Mirada y Parpadeo)
                is_forward = (t % 8) > 5  # Mira al frente los últimos 3 s de cada ciclo de 8 s
                is_blink = (t % 4) < 0.15 # Parpadea durante 0.15s cada 4s
                
                if is_blink:
                    eyes = eyes_blink
                elif is_forward:
                    eyes = eyes_forward
                else:
                    eyes = eyes_screen
                    
                frame.paste(eyes, (0, by), eyes)
                
                # Capa 3: Boca (Sincronización Labial segun Visemas)
                vis = 'X'
                for cue in cues:
                    if cue['start'] <= t <= cue['end']:
                        vis = cue['value']
                        if vis in ['G', 'H']: 
                            vis = 'X'
                        break
                
                if vis not in mouths:
                    vis = 'X'
                m_img = mouths[vis]
                frame.paste(m_img, (0, by), m_img)
                
                # Capa 4: Manos (Animación de tipeo)
                if is_forward:
                    h_img = hands[1]
                else:
                    h_img = hands[int(t * 8) % 3 + 1]
                frame.paste(h_img, (0, by), h_img)
                
                # Capa 5: Pelo (Capa superior de profundidad)
                frame.paste(hair_img, (0, by), hair_img)
                
                return np.array(frame.convert("RGB"))
                
            video = VideoClip(make_frame, duration=duration)
            video = video.with_audio(audio_clip)
            clips.append(video)
            
        print("\n[*] Uniendo y renderizando video final...")
        final_video = concatenate_videoclips(clips)
        final_video.write_videofile("video_completo.mp4", fps=FPS, codec="libx264", audio_codec="aac")
        final_video.close()
        print("\n[+] Proceso finalizado con éxito. El video se guardó en 'video_completo.mp4'.")
    finally:
        # Liberación explícita de recursos y clips de MoviePy para prevenir leaks de descriptores de archivo
        for c in clips:
            try:
                c.close()
            except Exception:
                pass

if __name__ == "__main__":
    run_pipeline()
