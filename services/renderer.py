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
    Servicio de renderizado Simulador Purista de VS Code IDE.
    Renderiza a pantalla completa (1920x1080) un editor VS Code con tipeo en vivo por IA,
    panel lateral de archivos, terminal de comandos inferior y barra de estado.
    """
    def __init__(self, remotion_dir: Path, output_dir: Path):
        self.remotion_dir = Path(remotion_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.status: Dict[str, Any] = {
            "status": "idle",
            "progress": 0,
            "message": "Listo para generar video con VS Code Purist IDE Engine.",
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
        Ejecuta el renderizado purista de VS Code IDE.
        """
        self.cleanup_old_temp_files()

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_filename = f"vscode_video_{timestamp}.mp4"

        output_path = self.output_dir / output_filename
        self.status["status"] = "rendering"
        self.status["progress"] = 10
        self.status["message"] = "Iniciando motor VS Code Purist IDE Engine..."
        self.status["output_file"] = str(output_path)
        logger.info(f"Iniciando renderizado VS Code Purist: {output_path}")

        if on_progress:
            await on_progress(self.status)

        try:
            if props_file_path and Path(props_file_path).exists():
                script = json.loads(Path(props_file_path).read_text(encoding="utf-8"))
            else:
                script = {"title": "Tutorial VS Code", "scenes": []}

            from moviepy import VideoClip, AudioFileClip, concatenate_videoclips

            scenes = script.get("scenes", [])
            clips = []
            total_scenes = len(scenes)

            for i, scene in enumerate(scenes):
                pct = min(90, 15 + int(((i + 1) / max(1, total_scenes)) * 75))
                self.status["progress"] = pct
                self.status["message"] = f"Compilando escena IDE {i+1}/{total_scenes}..."
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

                filename = scene.get("filename", "main.py")
                speech_text = scene.get("speechText", "")
                code_lines = scene.get("codeLines", ["# Script principal de desarrollo", "def run():", "    print('Ejecutando código...')"])

                # Renderizador Purista de VS Code IDE 1920x1080
                def make_frame(t):
                    canvas = Image.new("RGBA", (1920, 1080), (30, 30, 30, 255))
                    draw = ImageDraw.Draw(canvas)

                    # 1. Activity Bar (Extremo Izquierdo: 60px)
                    draw.rectangle([0, 0, 60, 1040], fill=(51, 51, 51, 255))
                    draw.text((18, 20), "📁", fill=(255, 255, 255, 255))
                    draw.text((18, 70), "🔍", fill=(150, 150, 150, 255))
                    draw.text((18, 120), "🌿", fill=(150, 150, 150, 255))
                    draw.text((18, 170), "⚙️", fill=(150, 150, 150, 255))

                    # 2. Sidebar Explorador (60px a 340px)
                    draw.rectangle([60, 0, 340, 1040], fill=(37, 37, 38, 255))
                    draw.text((80, 15), "EXPLORADOR: PROYECTO", fill=(180, 180, 180, 255))
                    draw.text((80, 50), "📂 src/", fill=(200, 200, 200, 255))
                    draw.text((100, 80), f"📄 {filename}", fill=(86, 156, 214, 255))
                    draw.text((100, 110), "📄 config.json", fill=(150, 150, 150, 255))
                    draw.text((100, 140), "📄 Dockerfile", fill=(150, 150, 150, 255))

                    # 3. Editor Tabs Bar (340px a 1920px, Alto 40px)
                    draw.rectangle([340, 0, 1920, 40], fill=(45, 45, 45, 255))
                    draw.rectangle([340, 0, 540, 40], fill=(30, 30, 30, 255))
                    draw.line([340, 0, 540, 0], fill=(0, 122, 204, 255), width=2)
                    draw.text((360, 10), f"🐍 {filename}", fill=(255, 255, 255, 255))

                    # 4. Code Area (340px a 1920px, 40px a 760px)
                    draw.rectangle([340, 40, 1920, 760], fill=(30, 30, 30, 255))
                    y_p = 60
                    for idx, line in enumerate(code_lines[:20]):
                        # Tipeo animado en vivo carácter por carácter
                        chars_to_show = int(min(len(line), max(0, (t * 24) - (idx * 4))))
                        # Número de línea
                        draw.text((360, y_p), f"{idx+1:2d}", fill=(133, 133, 133, 255))
                        # Contenido de código tipeado
                        draw.text((410, y_p), line[:chars_to_show], fill=(220, 220, 170, 255))
                        
                        # Cursor parpadeante en la última línea en escritura
                        if chars_to_show < len(line) or idx == len(code_lines) - 1:
                            if int(t * 4) % 2 == 0:
                                draw.rectangle([410 + len(line[:chars_to_show]) * 9, y_p, 410 + len(line[:chars_to_show]) * 9 + 8, y_p + 18], fill=(255, 255, 255, 255))
                        y_p += 32

                    # 5. Integrated Terminal Panel (340px a 1920px, 760px a 1040px)
                    draw.rectangle([340, 760, 1920, 1040], fill=(24, 24, 24, 255))
                    draw.line([340, 760, 1920, 760], fill=(60, 60, 60, 255), width=2)
                    draw.text((360, 770), "TERMINAL  |  PROBLEMS  |  OUTPUT  |  DEBUG CONSOLE", fill=(200, 200, 200, 255))
                    draw.text((360, 805), f"PS C:\\Users\\Dev\\Project> python {filename}", fill=(56, 189, 248, 255))
                    draw.text((360, 835), "[+] Ejecutando script... Procesamiento completado con éxito.", fill=(74, 222, 128, 255))

                    # 6. Bottom Status Bar (0px a 1920px, 1040px a 1080px)
                    draw.rectangle([0, 1040, 1920, 1080], fill=(0, 122, 204, 255))
                    draw.text((20, 1050), " 🌿 main*  |  UTF-8  |  Python 3.14  |  Prettier  |  100% Green", fill=(255, 255, 255, 255))

                    # Subtítulos translúcidos en pantalla
                    if speech_text:
                        draw.rectangle([400, 970, 1860, 1030], fill=(15, 23, 42, 240), outline=(56, 189, 248, 150), width=1)
                        draw.text((430, 990), speech_text[:110], fill=(255, 255, 255, 255))

                    return np.array(canvas.convert("RGB"))

                clip = VideoClip(make_frame, duration=duration)
                if audio_clip:
                    clip = clip.with_audio(audio_clip)

                clips.append(clip)

            self.status["progress"] = 92
            self.status["message"] = "Renderizando video VS Code Purist MP4..."
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
            self.status["message"] = f"¡Video MP4 generado exitosamente con VS Code Purist Engine en {output_filename}!"
            logger.info(f"Renderizado VS Code purista completado: {output_path}")

            if on_progress:
                await on_progress(self.status)
        except Exception as e:
            self.status["status"] = "error"
            self.status["message"] = f"Error en VS Code Purist Engine: {str(e)}"
            logger.error(f"Excepcion en renderizado VS Code purista: {e}")
            if on_progress:
                await on_progress(self.status)

        return self.status
