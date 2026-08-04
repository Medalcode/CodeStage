import os
import glob
import shutil
import subprocess
from pathlib import Path

OUTPUT_DIR = "../resultados_finales" if os.path.exists("../resultados_finales") else "resultados_finales"
FINAL_VIDEO = "video_completo.mp4"
LIST_FILE = "lista_temporal.txt"

def build_concat_list(output_dir=OUTPUT_DIR, list_file=LIST_FILE):
    """Busca los videos generados, los ordena y crea el archivo de lista para FFmpeg."""
    if not os.path.exists(output_dir):
        print(f"[!] La carpeta '{output_dir}' no existe.")
        return False

    search_pattern = os.path.join(output_dir, "**", "*.mp4")
    videos = glob.glob(search_pattern, recursive=True)
    
    # Excluir el archivo final de la lista si está dentro de la misma carpeta
    abs_final = str(Path(FINAL_VIDEO).resolve())
    videos = [v for v in videos if str(Path(v).resolve()) != abs_final]

    if not videos:
        print(f"[!] No se encontraron clips mp4 para unir en '{output_dir}'.")
        return False

    videos.sort(key=os.path.getmtime)

    with open(list_file, 'w', encoding='utf-8') as f:
        for video in videos:
            ruta_segura = Path(video).resolve().as_posix()
            f.write(f"file '{ruta_segura}'\n")
            
    print(f"[*] Se encontraron {len(videos)} clips. Lista generada en '{list_file}'.")
    return True

def concat_videos(list_file=LIST_FILE, final_video=FINAL_VIDEO):
    """Ejecuta FFmpeg para concatenar los videos sin re-codificar (demuxer concat)."""
    if not shutil.which("ffmpeg"):
        print("[!] FFmpeg no está instalado o no se encuentra disponible en el PATH del sistema.")
        return False

    abs_final = str(Path(final_video).resolve())
    print(f"[*] Uniendo clips con FFmpeg hacia '{abs_final}'...")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        abs_final
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n[+] ¡Éxito! El video final se guardó como: {abs_final}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al ejecutar FFmpeg: {e}")
        return False
    finally:
        if os.path.exists(list_file):
            try:
                os.remove(list_file)
            except Exception:
                pass

def main():
    if build_concat_list():
        concat_videos()

if __name__ == "__main__":
    main()
