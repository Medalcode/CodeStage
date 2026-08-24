import os
import sys
import time
import json
import asyncio
import math
import subprocess
from pathlib import Path
from typing import Dict, Any, Callable, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from logger import get_logger
from utils import ensure_dir, get_rhubarb_path

logger = get_logger("services.renderer")

class PythonSpriteCompositorRendererService:
    """
    Servicio de renderizado nativo en Python 40/60 Split-Screen.
    Combina Avatar 2D animado a la izquierda (40%) con un Canvas dinámico en la derecha (60%).
    """
    def __init__(self, remotion_dir: Path, output_dir: Path):
        self.remotion_dir = Path(remotion_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.status: Dict[str, Any] = {
            "status": "idle",
            "progress": 0,
            "message": "Listo para generar video.",
            "output_file": "",
        }

    def cleanup_old_temp_files(self, max_age_seconds: int = 86400) -> int:
        """Limpia archivos temporales antiguos."""
        cleaned_count = 0
        now = time.time()
        for folder in [self.remotion_dir, self.output_dir]:
            if not folder or not folder.exists():
                continue
            for pattern in ["*.tmp", "out_*.png", "out.png", "*.wav", "temp_*.mp4"]:
                for path in folder.glob(pattern):
                    try:
                        if path.is_file() and (now - path.stat().st_mtime) > max_age_seconds:
                            path.unlink()
                            cleaned_count += 1
                    except Exception as e:
                        logger.error(f"Error eliminando temporal {path}: {e}")
        return cleaned_count

    async def render(
        self,
        composition_id: str = "ExpressApiVideo",
        props_file_path: Optional[Path] = None,
        output_filename: Optional[str] = None,
        on_progress: Optional[Callable[[dict], Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta el renderizado nativo en Python usando MoviePy, PIL y FFmpeg.
        """
        self.cleanup_old_temp_files()

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_filename = f"video_{timestamp}.mp4"

        output_path = self.output_dir / output_filename
        self.status["status"] = "rendering"
        self.status["progress"] = 10
        self.status["message"] = "Iniciando motor de composición 40/60 nativo en Python..."
        self.status["output_file"] = str(output_path)
        logger.info(f"Iniciando renderizado nativo en Python: {output_path}")

        if on_progress:
            await on_progress(self.status)

        try:
            # Leer el guion JSON de entrada
            if props_file_path and Path(props_file_path).exists():
                script = json.loads(Path(props_file_path).read_text(encoding="utf-8"))
            else:
                script = {"title": "Tutorial", "scenes": []}

            # Importar MoviePy de forma diferida
            from moviepy import VideoClip, AudioFileClip, concatenate_videoclips

            # Cargar assets del avatar
            assets_dir = Path("assets").resolve()
            if not (assets_dir / "body.png").exists():
                from preparar_personaje import setup_assets
                setup_assets(output_dir=assets_dir)

            body_img = Image.open(assets_dir / 'body.png').convert("RGBA")
            hair_img = Image.open(assets_dir / 'hair.png').convert("RGBA")
            eyes_forward = Image.open(assets_dir / 'eyes' / 'eyes_forward.png').convert("RGBA")
            eyes_screen = Image.open(assets_dir / 'eyes' / 'eyes_screen.png').convert("RGBA")
            eyes_blink = Image.open(assets_dir / 'eyes' / 'eyes_blink.png').convert("RGBA")
            mouths = {
                shape: Image.open(assets_dir / 'mouth' / f'mouth_{shape}.png').convert("RGBA") 
                for shape in ['A', 'B', 'C', 'D', 'E', 'F', 'X']
            }
            hands = {
                1: Image.open(assets_dir / 'hands' / 'hands_type_1.png').convert("RGBA"),
                2: Image.open(assets_dir / 'hands' / 'hands_type_2.png').convert("RGBA"),
                3: Image.open(assets_dir / 'hands' / 'hands_type_3.png').convert("RGBA"),
            }

            rhubarb_exe = get_rhubarb_path()
            scenes = script.get("scenes", [])
            clips = []
            total_scenes = len(scenes)

            for i, scene in enumerate(scenes):
                pct = min(90, 15 + int(((i + 1) / max(1, total_scenes)) * 75))
                self.status["progress"] = pct
                self.status["message"] = f"Compilando escena {i+1}/{total_scenes} ({scene.get('type', 'scene')})..."
                if on_progress:
                    await on_progress(self.status)

                audio_file = scene.get("audioFile")
                duration = max(4.0, (scene.get("durationInFrames", 240) / 30.0))
                cues = []

                if audio_file:
                    audio_pub_path = Path("remotion-app/public/audio") / audio_file
                    if audio_pub_path.exists():
                        # Convertir MP3 a WAV para Rhubarb
                        wav_path = self.output_dir / f"scene_{i}.wav"
                        subprocess.run([
                            "ffmpeg", "-y", "-i", str(audio_pub_path), 
                            "-acodec", "pcm_s16le", "-ar", "16000", str(wav_path)
                        ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
                        if wav_path.exists() and os.path.exists(rhubarb_exe):
                            viseme_path = self.output_dir / f"visemes_{i}.json"
                            subprocess.run([
                                rhubarb_exe, "-f", "json", "-o", str(viseme_path), str(wav_path)
                            ], check=False, stdout=subprocess.DEVNULL)

                            if viseme_path.exists():
                                try:
                                    cues = json.loads(viseme_path.read_text(encoding="utf-8")).get('mouthCues', [])
                                except Exception:
                                    pass
                        
                        audio_clip = AudioFileClip(str(audio_pub_path))
                        duration = audio_clip.duration
                    else:
                        audio_clip = None
                else:
                    audio_clip = None

                scene_type = scene.get("type", "intro")
                scene_title = scene.get("title", "Tutorial")
                speech_text = scene.get("speechText", "")

                # Renderizador de frame 1920x1080 (Split 40/60)
                def make_frame(t):
                    full_canvas = Image.new("RGBA", (1920, 1080), (15, 23, 42, 255))
                    draw = ImageDraw.Draw(full_canvas)

                    # --- LADO IZQUIERDO (40% - 768px): AVATAR ---
                    avatar_frame = Image.new("RGBA", body_img.size, (0, 0, 0, 0))
                    by = int(math.sin(t * 2 * math.pi / 3.0) * 3)
                    avatar_frame.paste(body_img, (0, by), body_img)

                    is_forward = (t % 6) > 4
                    is_blink = (t % 3.5) < 0.15
                    eyes = eyes_blink if is_blink else (eyes_forward if is_forward else eyes_screen)
                    avatar_frame.paste(eyes, (0, by), eyes)

                    vis = 'X'
                    for cue in cues:
                        if cue['start'] <= t <= cue['end']:
                            vis = cue['value']
                            if vis in ['G', 'H']: vis = 'X'
                            break
                    m_img = mouths.get(vis, mouths['X'])
                    avatar_frame.paste(m_img, (0, by), m_img)

                    h_img = hands[1] if is_forward else hands[int(t * 8) % 3 + 1]
                    avatar_frame.paste(h_img, (0, by), h_img)
                    avatar_frame.paste(hair_img, (0, by), hair_img)

                    # Escalar Avatar al panel izquierdo de 768x1080
                    avatar_resized = avatar_frame.resize((768, 768), Image.Resampling.LANCZOS)
                    full_canvas.paste(avatar_resized, (0, 150), avatar_resized)

                    # Divider Vertical Line
                    draw.line([768, 0, 768, 1080], fill=(56, 189, 248, 100), width=3)

                    # --- LADO DERECHO (60% - 1152px): CANVAS DE TUTORIAL ---
                    draw.rounded_rectangle([810, 60, 1870, 950], radius=16, fill=(30, 41, 59, 255), outline=(56, 189, 248, 120), width=2)
                    draw.rectangle([810, 60, 1870, 120], fill=(51, 65, 85, 255))
                    draw.ellipse([830, 82, 846, 98], fill=(239, 68, 68, 255))
                    draw.ellipse([856, 82, 872, 98], fill=(245, 158, 11, 255))
                    draw.ellipse([882, 82, 898, 98], fill=(16, 185, 129, 255))

                    draw.text((920, 78), f"🎬 {scene_title}", fill=(248, 250, 252, 255))

                    if scene_type == "editor":
                        code_lines = scene.get("codeLines", ["// Código principal"])
                        y_pos = 160
                        draw.text((840, y_pos), f"📝 {scene.get('filename', 'script.py')}", fill=(56, 189, 248, 255))
                        y_pos += 40
                        for idx, line in enumerate(code_lines[:18]):
                            draw.text((840, y_pos), f"{idx+1:2d} | {line}", fill=(226, 232, 240, 255))
                            y_pos += 34
                    elif scene_type == "terminal":
                        y_pos = 160
                        draw.text((840, y_pos), "💻 CONSOLA DE COMANDOS", fill=(16, 185, 129, 255))
                        y_pos += 40
                        for cmd in scene.get("commands", []):
                            draw.text((840, y_pos), f"$ {cmd.get('text', '')}", fill=(56, 189, 248, 255))
                            y_pos += 30
                            for out in cmd.get("output", []):
                                draw.text((860, y_pos), out, fill=(148, 163, 184, 255))
                                y_pos += 26
                    elif scene_type == "excel":
                        y_pos = 160
                        draw.text((840, y_pos), f"📊 HOJA DE CÁLCULO: {scene.get('sheetName', 'Ventas')}", fill=(52, 211, 153, 255))
                        y_pos += 40
                        draw.text((840, y_pos), f"fx {scene.get('formula', '=SUMA()')}", fill=(110, 231, 183, 255))
                        y_pos += 40
                        headers = scene.get("headers", ["ID", "Producto", "Ventas"])
                        draw.text((840, y_pos), " | ".join(headers), fill=(255, 255, 255, 255))
                        y_pos += 35
                        for row in scene.get("rows", [])[:6]:
                            draw.text((840, y_pos), " | ".join([str(c) for c in row]), fill=(203, 213, 225, 255))
                            y_pos += 32
                    else:
                        draw.text((840, 200), scene_title, fill=(56, 189, 248, 255))
                        sub = scene.get("subtitle", "")
                        if sub:
                            draw.text((840, 250), sub, fill=(148, 163, 184, 255))

                    if speech_text:
                        draw.rectangle([60, 980, 1860, 1050], fill=(15, 23, 42, 230), outline=(56, 189, 248, 150), width=1)
                        draw.text((90, 1000), speech_text[:110], fill=(255, 255, 255, 255))

                    return np.array(full_canvas.convert("RGB"))

                clip = VideoClip(make_frame, duration=duration)
                if audio_clip:
                    clip = clip.with_audio(audio_clip)

                clips.append(clip)

            self.status["progress"] = 92
            self.status["message"] = "Renderizando y concatenando video final MP4..."
            if on_progress:
                await on_progress(self.status)

            final_video = concatenate_videoclips(clips)
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec="libx264",
                audio_codec="aac",
                logger=None
            )
            final_video.close()

            for c in clips:
                try:
                    c.close()
                except Exception:
                    pass

            self.status["status"] = "success"
            self.status["progress"] = 100
            self.status["message"] = f"¡Video MP4 generado exitosamente con motor Python nativo en {output_filename}!"
            logger.info(f"Renderizado nativo en Python completado con éxito: {output_path}")

            if on_progress:
                await on_progress(self.status)
        except Exception as e:
            self.status["status"] = "error"
            self.status["message"] = f"Error en renderizado Python nativo: {str(e)}"
            logger.error(f"Excepcion en renderizado nativo Python: {e}")
            if on_progress:
                await on_progress(self.status)

        return self.status

# Alias polimórfico para 100% retrocompatibilidad con la API
RemotionRendererService = PythonSpriteCompositorRendererService
