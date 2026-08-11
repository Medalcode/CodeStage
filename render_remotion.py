import os
import subprocess
import sys
from pathlib import Path

REMOTION_DIR = Path(__file__).parent / "remotion-app"
OUTPUT_VIDEO = Path(__file__).parent / "video_completo_remotion.mp4"

def render_video(composition_id="TutorialVideo"):
    """
    Ejecuta el renderizado de Remotion compilando los componentes de React a MP4.
    """
    if not REMOTION_DIR.exists():
        print(f"[!] No se encontró el directorio de Remotion en '{REMOTION_DIR}'.")
        return False

    print(f"[*] Iniciando renderizado de Remotion para la composición '{composition_id}'...")
    cmd = [
        "npx.cmd" if sys.platform.startswith("win") else "npx",
        "remotion",
        "render",
        composition_id,
        str(OUTPUT_VIDEO.resolve())
    ]

    try:
        subprocess.run(cmd, cwd=str(REMOTION_DIR), check=True)
        print(f"\n[+] ¡Éxito! El video de Remotion se guardó en: {OUTPUT_VIDEO.resolve()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al renderizar video con Remotion: {e}")
        return False

if __name__ == "__main__":
    render_video()
