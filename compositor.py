import os
import json
import subprocess
import math
import numpy as np
from PIL import Image
from moviepy import VideoClip, AudioFileClip, concatenate_videoclips

# Configuration
GUION_FILE = "guion.txt"
OUTPUT_DIR = "resultados_finales"
VOICE = "es-MX-DaliaNeural"
FPS = 24

print("[*] Cargando assets de imagen...")
try:
    body_img = Image.open('assets/body.png').convert("RGBA")
    hair_img = Image.open('assets/hair.png').convert("RGBA")
    
    eyes_forward = Image.open('assets/eyes/eyes_forward.png').convert("RGBA")
    eyes_screen = Image.open('assets/eyes/eyes_screen.png').convert("RGBA")
    eyes_blink = Image.open('assets/eyes/eyes_blink.png').convert("RGBA")
    
    mouths = {
        shape: Image.open(f'assets/mouth/mouth_{shape}.png').convert("RGBA") 
        for shape in ['A', 'B', 'C', 'D', 'E', 'F', 'X']
    }
    
    hands = {
        1: Image.open('assets/hands/hands_type_1.png').convert("RGBA"),
        2: Image.open('assets/hands/hands_type_2.png').convert("RGBA"),
        3: Image.open('assets/hands/hands_type_3.png').convert("RGBA"),
    }
except Exception as e:
    print(f"[!] Error cargando assets: {e}")
    print("Por favor, asegúrate de que los archivos existan en la carpeta assets/.")
    exit(1)

def split_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [c.strip() for c in f.read().split('\n\n') if c.strip()]

def run_pipeline():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    chunks = split_script(GUION_FILE)
    clips = []
    
    for i, text in enumerate(chunks, 1):
        print(f"\n======================================")
        print(f"[*] Procesando bloque {i}/{len(chunks)}...")
        print(f"======================================")
        
        # 1. Audio
        audio_mp3_path = f"{OUTPUT_DIR}/audio_{i}.mp3"
        audio_path = f"{OUTPUT_DIR}/audio_{i}.wav"
        print(f"[*] Generando audio...")
        subprocess.run(["edge-tts", "--text", text, "--voice", VOICE, "--write-media", audio_mp3_path], check=True)
        
        # Convertir a WAV (requerido por Rhubarb) usando ffmpeg
        subprocess.run(["ffmpeg", "-y", "-i", audio_mp3_path, "-acodec", "pcm_s16le", "-ar", "16000", audio_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 2. Rhubarb
        viseme_path = f"{OUTPUT_DIR}/visemes_{i}.json"
        print(f"[*] Analizando audio para sincronización labial...")
        
        # Ruta al ejecutable de Rhubarb
        rhubarb_exe = os.path.join(os.getcwd(), "rhubarb", "Rhubarb-Lip-Sync-1.14.0-Windows", "rhubarb.exe")
        
        subprocess.run([
            rhubarb_exe, 
            "-f", "json", 
            "-o", viseme_path, 
            audio_path
        ], check=True, stdout=subprocess.DEVNULL)
        
        # Cargar visemas
        with open(viseme_path, 'r') as f:
            cues = json.load(f)['mouthCues']
            
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        def make_frame(t):
            # Crear frame base transparente
            frame = Image.new("RGBA", body_img.size, (255, 255, 255, 255))
            
            # Efecto de respiración (desplazamiento en Y)
            by = int(math.sin(t * 2 * math.pi / 3.0) * 2)
            
            # Pegar cuerpo
            frame.paste(body_img, (0, by), body_img)
            
            # Lógica de Mirada y Parpadeo
            is_forward = (t % 8) > 5  # Mira al frente los últimos 3 segs de cada ciclo de 8 segs
            is_blink = (t % 4) < 0.15 # Parpadea cada 4 segs durante 0.15s
            
            if is_blink:
                eyes = eyes_blink
            elif is_forward:
                eyes = eyes_forward
            else:
                eyes = eyes_screen
                
            frame.paste(eyes, (0, by), eyes)
            
            # Lógica de Sincronización Labial
            vis = 'X'
            for cue in cues:
                if cue['start'] <= t <= cue['end']:
                    vis = cue['value']
                    # Rhubarb a veces retorna visemas G o H en formatos extendidos, los mapeamos
                    if vis in ['G', 'H']: 
                        vis = 'X'
                    break
            
            if vis not in mouths:
                vis = 'X'
            m_img = mouths[vis]
            frame.paste(m_img, (0, by), m_img)
            
            # Lógica de Manos (Tipeando)
            if is_forward:
                # Si está mirando a la cámara, pausa el tipeo (manos en reposo)
                h_img = hands[1]
            else:
                # Animación de tipeo (3 frames a ~8fps)
                h_img = hands[int(t * 8) % 3 + 1]
            frame.paste(h_img, (0, by), h_img)
            
            # Pelo por encima de todo
            frame.paste(hair_img, (0, by), hair_img)
            
            # Retornar como array Numpy (requerido por MoviePy)
            return np.array(frame.convert("RGB"))
            
        # Crear clip de video
        video = VideoClip(make_frame, duration=duration)
        video = video.with_audio(audio_clip)
        clips.append(video)
        
    print("\n[*] Uniendo y renderizando video final...")
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("video_completo.mp4", fps=FPS, codec="libx264", audio_codec="aac")
    print("\n[+] Proceso finalizado. El video se guardó en video_completo.mp4")

if __name__ == "__main__":
    run_pipeline()
