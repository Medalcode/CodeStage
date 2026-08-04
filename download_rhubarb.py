import os
import sys
import json
import zipfile
import urllib.request
from pathlib import Path

def download_rhubarb(dest_dir="rhubarb"):
    """
    Descarga automáticamente la última versión de Rhubarb Lip Sync desde GitHub
    correspondiente a la plataforma (Windows, Linux o macOS).
    """
    api_url = "https://api.github.com/repos/DanielSWolf/rhubarb-lip-sync/releases/latest"
    print(f"[*] Obteniendo información de la última versión de Rhubarb Lip Sync...")
    
    target_keyword = "win" if sys.platform.startswith("win") else ("mac" if sys.platform == "darwin" else "linux")
    
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        download_url = None
        for asset in data.get('assets', []):
            name = asset['name'].lower()
            if target_keyword in name and name.endswith('.zip'):
                download_url = asset['browser_download_url']
                break
                
        if not download_url and data.get('assets'):
            # Fallback a cualquier zip disponible
            download_url = data['assets'][0]['browser_download_url']

        if download_url:
            print(f"[*] Descargando Rhubarb desde: {download_url}")
            zip_path = "rhubarb_tmp.zip"
            urllib.request.urlretrieve(download_url, zip_path)
            
            print(f"[*] Extrayendo ejecutable en '{dest_dir}/'...")
            dest_path = Path(dest_dir)
            dest_path.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dest_path)
                
            if os.path.exists(zip_path):
                os.remove(zip_path)
            print("[+] Descarga y extracción completadas con éxito.")
        else:
            print(f"[!] No se encontró un paquete comprimido compatible para '{target_keyword}'.")
    except Exception as e:
        print(f"[!] Error descargando Rhubarb Lip Sync: {e}")

if __name__ == "__main__":
    download_rhubarb()
