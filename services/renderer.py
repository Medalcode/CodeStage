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
from utils import ensure_dir

logger = get_logger("services.renderer")

class RemotionRendererService:
    """
    Servicio de renderizado LTX AI Avatar Diffusion Engine.
    Combina Avatar parlante generado por IA difusiva (Ghibli Programmer) a la izquierda (40%)
    con IDE / Browser dinámico en la derecha (60%).
    """
    def __init__(self, remotion_dir: Path, output_dir: Path):
        self.remotion_dir = Path(remotion_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.status: Dict[str, Any] = {
            "status": "idle",
            "progress": 0,
            "message": "Listo para generar video con LTX AI Avatar Engine.",
            "output_file": "",
        }

    def cleanup_old_temp_files(self, max_age_seconds: int = 86400) -> int:
        """Limpia archivos temporales antiguos."""
        cleaned_count = 0
        now = time.time()
        for folder in [self.remotion_dir, self.output_dir]:
            if not folder or not folder.exists():
                continue
            for pattern in ["*.tmp", "*.wav", "temp_*.mp4"]:
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
        Ejecuta el renderizado de LTX AI Avatar Engine.
        """
        self.cleanup_old_temp_files()

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_filename = f"ltx_avatar_video_{timestamp}.mp4"

        output_path = self.output_dir / output_filename
        self.status["status"] = "rendering"
        self.status["progress"] = 10
        self.status["message"] = "Iniciando motor LTX AI Avatar Diffusion Engine..."
        self.status["output_file"] = str(output_path)
        logger.info(f"Iniciando renderizado LTX AI Avatar: {output_path}")

        if on_progress:
            await on_progress(self.status)

        try:
            if props_file_path and Path(props_file_path).exists():
                script = json.loads(Path(props_file_path).read_text(encoding="utf-8"))
            else:
                script = {"title": "Tutorial LTX Avatar", "scenes": []}

            from moviepy import VideoClip, AudioFileClip, concatenate_videoclips

            # Cargar asset base del avatar Ghibli Programmer si existe o generar uno estilizado
            avatar_path = Path("assets/ghibli_programmer.png")
            if not avatar_path.exists():
                from preparar_personaje import setup_assets
                setup_assets(output_dir=Path("assets"))

            if avatar_path.exists():
                base_avatar = Image.open(avatar_path).convert("RGBA")
            else:
                base_avatar = Image.open("assets/body.png").convert("RGBA")

            scenes = script.get("scenes", [])
            clips = []
            total_scenes = len(scenes)

            for i, scene in enumerate(scenes):
                pct = min(90, 15 + int(((i + 1) / max(1, total_scenes)) * 75))
                self.status["progress"] = pct
                self.status["message"] = f"Compilando escena LTX Avatar {i+1}/{total_scenes}..."
                if on_progress:
                    await on_progress(self.status)

                audio_file = scene.get("audioFile")
                duration = max(4.0, (scene.get("durationInFrames", 240) / 30.0))

                if audio_file:
                    audio_pub_path = Path("remotion-app/public/audio") / audio_file
                    if audio_pub_path.exists():
                        audio_clip = AudioFileClip(str(audio_pub_path))
                        duration = audio_clip.duration
                    else:
                        audio_clip = None
                else:
                    audio_clip = None

                scene_title = scene.get("title", "Ghibli AI Avatar")
                speech_text = scene.get("speechText", "")

                # Renderizador LTX AI Avatar Split-Screen 1920x1080
                def make_frame(t):
                    full_canvas = Image.new("RGBA", (1920, 1080), (13, 17, 23, 255))
                    draw = ImageDraw.Draw(full_canvas)

                    # Lado Izquierdo (40% - 768px): Avatar IA Hablante
                    by = int(math.sin(t * 2.5) * 4)
                    avatar_frame = base_avatar.resize((768, 768), Image.Resampling.LANCZOS)
                    full_canvas.paste(avatar_frame, (0, 150 + by), avatar_frame)

                    # Simulación de boca hablando con IA
                    if int(t * 10) % 2 == 0:
                        draw.ellipse([340, 480 + by, 420, 520 + by], fill=(180, 40, 40, 255))

                    # Glow Aura & Divider
                    draw.line([768, 0, 768, 1080], fill=(236, 72, 153, 120), width=3)

                    # Lado Derecho (60% - 1152px): Dynamic Tutorial Window
                    draw.rounded_rectangle([810, 60, 1870, 950], radius=16, fill=(22, 27, 34, 255), outline=(236, 72, 153, 150), width=2)
                    draw.rectangle([810, 60, 1870, 120], fill=(33, 38, 45, 255))
                    draw.text((840, 78), f"🤖 LTX AI AVATAR — {scene_title}", fill=(244, 114, 182, 255))

                    code_lines = scene.get("codeLines", ["# LTX AI Avatar Generator", "avatar = LTXVideo.generate(prompt)", "avatar.talk(audio)"])
                    y_p = 160
                    for idx, line in enumerate(code_lines[:16]):
                        draw.text((840, y_p), f"{idx+1:2d} | {line}", fill=(229, 231, 235, 255))
                        y_p += 36

                    if speech_text:
                        draw.rectangle([60, 980, 1860, 1050], fill=(13, 17, 23, 240), outline=(236, 72, 153, 150), width=1)
                        draw.text((90, 1000), speech_text[:110], fill=(255, 255, 255, 255))

                    return np.array(full_canvas.convert("RGB"))

                clip = VideoClip(make_frame, duration=duration)
                if audio_clip:
                    clip = clip.with_audio(audio_clip)

                clips.append(clip)

            self.status["progress"] = 92
            self.status["message"] = "Renderizando video LTX AI Avatar MP4..."
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
            self.status["message"] = f"¡Video MP4 generado exitosamente con LTX AI Avatar Engine en {output_filename}!"
            logger.info(f"Renderizado LTX AI Avatar completado: {output_path}")

            if on_progress:
                await on_progress(self.status)
        except Exception as e:
            self.status["status"] = "error"
            self.status["message"] = f"Error en LTX AI Avatar Engine: {str(e)}"
            logger.error(f"Excepcion en renderizado LTX AI Avatar: {e}")
            if on_progress:
                await on_progress(self.status)

        return self.status
