import os
import shutil
import hashlib
import subprocess
from pathlib import Path
from utils.filesystem import ensure_dir

DEFAULT_VOICE = "es-MX-DaliaNeural"
BASE_DIR = Path(__file__).parent.parent.resolve()
CACHE_AUDIO_DIR = BASE_DIR / "cache" / "audio"
PUBLIC_AUDIO_DIR = BASE_DIR / "remotion-app" / "public" / "audio"

def get_audio_hash(text: str, voice: str = DEFAULT_VOICE) -> str:
    """Calcula el hash SHA-256 único a partir del texto y la voz."""
    key = f"{voice}::{text.strip()}".encode('utf-8')
    return hashlib.sha256(key).hexdigest()[:16]

def get_audio_duration_seconds(audio_path: str) -> float:
    """
    Calcula los segundos exactos de un archivo de audio MP3.
    """
    p = Path(audio_path)
    if not p.exists() or p.stat().st_size == 0:
        return 5.0

    # Intento 1: Usar ffprobe si está disponible en el sistema
    ffprobe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(p)]
    try:
        res = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        dur = float(res.stdout.strip())
        if dur > 0:
            return dur
    except Exception:
        pass

    # Intento 2: Estimación por bitrate de edge-tts (~64kbps / 8000 bytes por segundo)
    file_size_bytes = p.stat().st_size
    estimated_seconds = max(3.0, file_size_bytes / 6500.0)
    return estimated_seconds

def generate_audio(text: str, output_path: str, voice: str = DEFAULT_VOICE, use_cache: bool = True) -> str:
    """
    Genera un archivo de audio TTS usando edge-tts con soporte de caché por hash MD5.
    """
    if not text or not text.strip():
        return None

    out_p = Path(output_path)
    ensure_dir(out_p.parent)

    if use_cache:
        ensure_dir(CACHE_AUDIO_DIR)
        audio_hash = get_audio_hash(text, voice)
        cached_file = CACHE_AUDIO_DIR / f"{audio_hash}.mp3"

        if cached_file.exists() and cached_file.stat().st_size > 0:
            print(f"[*] Usando audio en caché para: '{text[:30]}...' ({audio_hash[:8]})")
            shutil.copy(cached_file, out_p)
            return str(out_p)

    cmd = [
        "edge-tts", 
        "--text", text, 
        "--voice", voice, 
        "--write-media", str(out_p)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if use_cache:
            shutil.copy(out_p, CACHE_AUDIO_DIR / f"{get_audio_hash(text, voice)}.mp3")
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"Error al generar audio con edge-tts: {stderr_msg}") from e
    return str(out_p)

def prepare_script_audio(script: dict, voice: str = DEFAULT_VOICE) -> dict:
    """
    Sintetiza los audios para cada escena del guion, mide su duración real
    y asigna durationInFrames a cada escena para sincronización perfecta en Remotion.
    """
    ensure_dir(PUBLIC_AUDIO_DIR)
    scenes = script.get("scenes", [])

    for scene in scenes:
        speech_text = scene.get("speechText", "")
        scene_id = scene.get("id", "scene")
        audio_filename = f"audio_{scene_id}.mp3"
        audio_out_path = PUBLIC_AUDIO_DIR / audio_filename

        if speech_text.strip():
            try:
                generated = generate_audio(speech_text, audio_out_path, voice=voice)
                if generated:
                    scene["audioFile"] = audio_filename
                    duration_sec = get_audio_duration_seconds(audio_out_path)
                    # Asignar fotogramas dinámicos (30 fps + 1.2s de margen visual)
                    scene["durationInFrames"] = max(180, int((duration_sec + 1.2) * 30))
                else:
                    scene["audioFile"] = None
                    scene["durationInFrames"] = scene.get("durationInFrames", 240)
            except Exception as e:
                print(f"[!] Warning: no se pudo sintetizar audio para la escena {scene_id}: {e}")
                scene["audioFile"] = None
                scene["durationInFrames"] = scene.get("durationInFrames", 240)
        else:
            scene["audioFile"] = None
            scene["durationInFrames"] = scene.get("durationInFrames", 240)

    return script
