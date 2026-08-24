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
    Servicio de renderizado de Animaciones Vectoriales con Manim Engine (Estilo 3Blue1Brown).
    Genera animaciones de código, nodos y diagramas vectoriales cuadro a cuadro.
    """
    def __init__(self, remotion_dir: Path, output_dir: Path):
        self.remotion_dir = Path(remotion_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.status: Dict[str, Any] = {
            "status": "idle",
            "progress": 0,
            "message": "Listo para generar video con Manim Vector Engine.",
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
        Ejecuta el renderizado vectorial Manim de código y diagramas.
        """
        self.cleanup_old_temp_files()

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_filename = f"manim_video_{timestamp}.mp4"

        output_path = self.output_dir / output_filename
        self.status["status"] = "rendering"
        self.status["progress"] = 10
        self.status["message"] = "Iniciando motor Manim Vector Engine..."
        self.status["output_file"] = str(output_path)
        logger.info(f"Iniciando renderizado Manim Vector: {output_path}")

        if on_progress:
            await on_progress(self.status)

        try:
            if props_file_path and Path(props_file_path).exists():
                script = json.loads(Path(props_file_path).read_text(encoding="utf-8"))
            else:
                script = {"title": "Tutorial Manim", "scenes": []}

            from moviepy import VideoClip, AudioFileClip, concatenate_videoclips

            scenes = script.get("scenes", [])
            clips = []
            total_scenes = len(scenes)

            for i, scene in enumerate(scenes):
                pct = min(90, 15 + int(((i + 1) / max(1, total_scenes)) * 75))
                self.status["progress"] = pct
                self.status["message"] = f"Compilando animación Manim {i+1}/{total_scenes}..."
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

                scene_title = scene.get("title", "Animación Vectorial")
                speech_text = scene.get("speechText", "")
                scene_type = scene.get("type", "intro")

                # Frame Renderer estilo Manim / 3Blue1Brown
                def make_frame(t):
                    canvas = Image.new("RGBA", (1920, 1080), (10, 15, 26, 255))
                    draw = ImageDraw.Draw(canvas)

                    # Vector Grid Lines en fondo
                    grid_alpha = 40
                    for x in range(0, 1920, 80):
                        draw.line([x, 0, x, 1080], fill=(30, 58, 138, grid_alpha), width=1)
                    for y in range(0, 1080, 80):
                        draw.line([0, y, 1920, y], fill=(30, 58, 138, grid_alpha), width=1)

                    # Manim Glowing Header Title
                    draw.text((100, 70), f"📐 MANIM VECTOR ENGINE — {scene_title}", fill=(56, 189, 248, 255))

                    # Animated Progress Math Circle / Node Diagram
                    cx, cy = 1450, 450
                    radius = 180 + int(math.sin(t * 3) * 10)
                    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=(147, 51, 234, 255), width=3)
                    draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(88, 28, 135, 180), outline=(192, 132, 252, 255), width=2)
                    draw.text((cx - 40, cy - 10), "f(x) → y", fill=(255, 255, 255, 255))

                    # Vector Code Box
                    draw.rounded_rectangle([100, 160, 1150, 880], radius=16, fill=(17, 24, 39, 230), outline=(56, 189, 248, 150), width=2)
                    draw.rectangle([100, 160, 1150, 220], fill=(31, 41, 55, 255))
                    draw.text((130, 180), f"⚙️ {scene_type.upper()} MODULE", fill=(16, 185, 129, 255))

                    lines = scene.get("codeLines", ["# Algoritmo en proceso", "def solve(matrix):", "    return np.linalg.det(matrix)"])
                    y_p = 260
                    for idx, l in enumerate(lines[:16]):
                        # Animation Reveal effect based on time t
                        chars_to_show = int(min(len(l), max(0, (t * 20) - (idx * 5))))
                        draw.text((140, y_p), f"{idx+1:2d} | {l[:chars_to_show]}", fill=(229, 231, 235, 255))
                        y_p += 36

                    if speech_text:
                        draw.rectangle([80, 950, 1840, 1030], fill=(17, 24, 39, 240), outline=(168, 85, 247, 150), width=1)
                        draw.text((110, 975), speech_text[:110], fill=(255, 255, 255, 255))

                    return np.array(canvas.convert("RGB"))

                clip = VideoClip(make_frame, duration=duration)
                if audio_clip:
                    clip = clip.with_audio(audio_clip)

                clips.append(clip)

            self.status["progress"] = 92
            self.status["message"] = "Renderizando y concatenando video Manim MP4..."
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
            self.status["message"] = f"¡Video MP4 generado exitosamente con Manim Vector Engine en {output_filename}!"
            logger.info(f"Renderizado Manim completado: {output_path}")

            if on_progress:
                await on_progress(self.status)
        except Exception as e:
            self.status["status"] = "error"
            self.status["message"] = f"Error en Manim Vector Engine: {str(e)}"
            logger.error(f"Excepcion en renderizado Manim: {e}")
            if on_progress:
                await on_progress(self.status)

        return self.status
