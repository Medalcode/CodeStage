import sys
import time
import asyncio
import subprocess
import re
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from logger import get_logger

logger = get_logger("services.renderer")

class RemotionRendererService:
    """
    Servicio de renderizado desacoplado para compilar composiciones de Remotion en React a MP4.
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
        """
        Limpia archivos temporales y renders de vista previa antiguos (> 24 horas).
        """
        cleaned_count = 0
        now = time.time()

        for pattern in ["*.tmp", "out_*.png", "out.png"]:
            for path in self.remotion_dir.glob(pattern):
                try:
                    if path.is_file() and (now - path.stat().st_mtime) > max_age_seconds:
                        path.unlink()
                        cleaned_count += 1
                except Exception as e:
                    logger.error(f"Error eliminando temporal {path}: {e}")

        if cleaned_count > 0:
            logger.info(f"Limpieza completada: {cleaned_count} temporales eliminados.")
        return cleaned_count

    async def render(
        self,
        composition_id: str = "ExpressApiVideo",
        props_file_path: Optional[Path] = None,
        output_filename: Optional[str] = None,
        on_progress: Optional[Callable[[dict], Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta el renderizado de Remotion de forma asíncrona generando un archivo único.
        """
        self.cleanup_old_temp_files()

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_filename = f"video_{timestamp}.mp4"

        output_path = self.output_dir / output_filename
        self.status["status"] = "rendering"
        self.status["progress"] = 25
        self.status["message"] = f"Iniciando compilador de Remotion React ({composition_id})..."
        self.status["output_file"] = str(output_path)
        logger.info(f"Iniciando renderizado Remotion en: {output_path}")

        if on_progress:
            await on_progress(self.status)

        try:
            if sys.platform.startswith("win"):
                cmd = ["cmd.exe", "/c", "npx", "remotion", "render", composition_id, str(output_path)]
            else:
                cmd = ["npx", "remotion", "render", composition_id, str(output_path)]

            if props_file_path and Path(props_file_path).exists():
                cmd.append(f"--props={str(props_file_path)}")

            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.remotion_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )

            buffer = ""
            while True:
                chunk = await process.stdout.read(1024)
                if not chunk:
                    break
                
                buffer += chunk.decode('utf-8', errors='ignore')
                lines = re.split(r'[\r\n]+', buffer)
                buffer = lines.pop() if len(lines) > 1 else buffer

                for line_str in lines:
                    line_str = line_str.strip()
                    if not line_str:
                        continue

                    logger.info(f"[Remotion] {line_str}")

                    # 1. Match Rendered X/Y progress
                    rendered_match = re.search(r'Rendered\s+(\d+)/(\d+)', line_str)
                    if rendered_match:
                        current_frame = int(rendered_match.group(1))
                        total_frames = int(rendered_match.group(2))
                        if total_frames > 0:
                            percent = min(99, int(25 + (current_frame / total_frames) * 74))
                            self.status["progress"] = percent
                            self.status["message"] = f"Renderizando fotogramas con voz: {current_frame}/{total_frames} ({percent}%)"
                            if on_progress:
                                await on_progress(self.status)

                    # 2. Match Bundling X% progress
                    elif "Bundling" in line_str:
                        bundling_match = re.search(r'Bundling\s+(\d+)%', line_str)
                        if bundling_match:
                            percent = min(25, int(int(bundling_match.group(1)) * 0.25))
                            self.status["progress"] = percent
                            self.status["message"] = f"Compilando escenas en React ({bundling_match.group(1)}%)..."
                            if on_progress:
                                await on_progress(self.status)

            await process.wait()

            if process.returncode == 0:
                self.status["status"] = "success"
                self.status["progress"] = 100
                self.status["message"] = f"¡Video MP4 generado exitosamente en {output_filename}!"
                logger.info(f"Renderizado completado con éxito: {output_path}")
            else:
                self.status["status"] = "error"
                self.status["message"] = "Error durante el renderizado de Remotion."
                logger.error("Falló el subproceso de renderizado de Remotion.")

            if on_progress:
                await on_progress(self.status)
        except Exception as e:
            self.status["status"] = "error"
            self.status["message"] = str(e)
            logger.error(f"Excepcion en renderizado: {e}")
            if on_progress:
                await on_progress(self.status)

        return self.status
