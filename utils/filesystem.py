import os
import shutil
from pathlib import Path

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

def get_rhubarb_path(base_dir=None):
    """
    Retorna la ruta al ejecutable de Rhubarb Lip Sync según el sistema operativo.
    Busca primero en la carpeta local 'rhubarb/' y luego en el PATH del sistema.
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent
    else:
        base_dir = Path(base_dir)

    rhubarb_dir = base_dir / "rhubarb"
    if rhubarb_dir.exists():
        executables = list(rhubarb_dir.rglob("rhubarb.exe")) + list(rhubarb_dir.rglob("rhubarb"))
        for exe in executables:
            if exe.is_file() and not exe.name.endswith(".zip"):
                return str(exe.resolve())

    system_rhubarb = shutil.which("rhubarb")
    if system_rhubarb:
        return system_rhubarb

    fallback = rhubarb_dir / "Rhubarb-Lip-Sync-1.14.0-Windows" / "rhubarb.exe"
    return str(fallback.resolve())
