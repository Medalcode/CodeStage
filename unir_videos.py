import os
import glob
import subprocess

# ==========================================
# CONFIGURACIÓN
# ==========================================
OUTPUT_DIR = "../resultados_finales"
FINAL_VIDEO = "../video_completo.mp4"
LIST_FILE = "lista_temporal.txt"

def build_concat_list():
    """Busca los videos generados, los ordena y crea el archivo para FFmpeg."""
    if not os.path.exists(OUTPUT_DIR):
        print(f"[!] La carpeta {OUTPUT_DIR} no existe.")
        return None

    # Buscar recursivamente todos los .mp4 dentro de la carpeta de resultados
    search_pattern = os.path.join(OUTPUT_DIR, "**", "*.mp4")
    videos = glob.glob(search_pattern, recursive=True)
    
    if not videos:
        print("[!] No se encontraron videos mp4 para unir.")
        return None

    # Ordenar los videos por fecha de modificación (para mantener el orden del guion)
    videos.sort(key=os.path.getmtime)

    # Crear el archivo de lista con la sintaxis requerida por FFmpeg: file 'ruta'
    with open(LIST_FILE, 'w', encoding='utf-8') as f:
        for video in videos:
            # Reemplazar barras invertidas en caso de usarse en otro SO y escapar rutas
            ruta_segura = os.path.abspath(video).replace('\\', '/')
            f.write(f"file '{ruta_segura}'\n")
            
    print(f"[*] Se encontraron {len(videos)} clips. Lista generada en {LIST_FILE}.")
    return True

def concat_videos():
    """Ejecuta FFmpeg para concatenar los videos sin re-codificar."""
    print("[*] Ejecutando FFmpeg para unir los clips...")
    
    # Usa ruta absoluta para el video final para evitar errores
    abs_final_video = os.path.abspath(FINAL_VIDEO)

    cmd = [
        "ffmpeg",
        "-y",                 # Sobrescribir si el archivo final ya existe
        "-f", "concat",       # Usar el demuxer de concatenación
        "-safe", "0",         # Permitir rutas absolutas en el archivo de lista
        "-i", LIST_FILE,      # Archivo de entrada con la lista
        "-c", "copy",         # Copiar los flujos de video/audio sin re-renderizar
        abs_final_video
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n[+] ¡Éxito! El video final se guardó como: {abs_final_video}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al ejecutar FFmpeg: {e}")
    finally:
        # Limpieza del archivo temporal
        if os.path.exists(LIST_FILE):
            os.remove(LIST_FILE)

def main():
    if build_concat_list():
        concat_videos()

if __name__ == "__main__":
    main()
