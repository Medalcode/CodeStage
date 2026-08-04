import os
import sys
import shutil
import subprocess
from pathlib import Path

DEFAULT_VOICE = "es-MX-DaliaNeural"

def ensure_dir(path):
    """Crea un directorio si no existe y retorna un objeto Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def split_script(file_path):
    """
    Divide el guion en bloques basados en dobles saltos de línea.
    Maneja diferentes codificaciones y limpia espacios en blanco.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"No se encontró el archivo de guion: {file_path}")
        
    text = ""
    for encoding in ('utf-8', 'utf-8-sig', 'latin-1'):
        try:
            text = p.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
            
    chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
    return chunks

def generate_audio(text, output_path, voice=DEFAULT_VOICE):
    """
    Genera un archivo de audio TTS usando edge-tts.
    """
    out_p = Path(output_path)
    ensure_dir(out_p.parent)
    
    cmd = [
        "edge-tts", 
        "--text", text, 
        "--voice", voice, 
        "--write-media", str(out_p)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"Error al generar audio con edge-tts: {stderr_msg}") from e
    return str(out_p)

def get_rhubarb_path(base_dir=None):
    """
    Retorna la ruta al ejecutable de Rhubarb Lip Sync según el sistema operativo.
    Busca primero en la carpeta local 'rhubarb/' y luego en el PATH del sistema.
    """
    if base_dir is None:
        base_dir = Path(__file__).parent
    else:
        base_dir = Path(base_dir)

    # 1. Buscar ejecutable local en la carpeta rhubarb/
    rhubarb_dir = base_dir / "rhubarb"
    if rhubarb_dir.exists():
        # Buscar ejecutable .exe en Windows o binario executable en Unix
        executables = list(rhubarb_dir.rglob("rhubarb.exe")) + list(rhubarb_dir.rglob("rhubarb"))
        for exe in executables:
            if exe.is_file() and not exe.name.endswith(".zip"):
                return str(exe.resolve())

    # 2. Buscar en el PATH del sistema
    system_rhubarb = shutil.which("rhubarb")
    if system_rhubarb:
        return system_rhubarb

    # Fallback por defecto si no se encuentra
    fallback = rhubarb_dir / "Rhubarb-Lip-Sync-1.14.0-Windows" / "rhubarb.exe"
    return str(fallback.resolve())
