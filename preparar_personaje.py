import os
import shutil
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import("PIL")
from PIL import Image, ImageDraw

def setup_assets():
    # Rutas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    mouth_dir = os.path.join(assets_dir, "mouth")
    eyes_dir = os.path.join(assets_dir, "eyes")
    hands_dir = os.path.join(assets_dir, "hands")
    
    # Crear carpetas si no existen
    os.makedirs(mouth_dir, exist_ok=True)
    os.makedirs(eyes_dir, exist_ok=True)
    os.makedirs(hands_dir, exist_ok=True)
    
    # Imagen generada
    # Usaremos una imagen base de color para simular si no encontramos la original
    width, height = 1024, 1024
    
    # 1. Cuerpo (Body) y Pelo
    body = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(body)
    # Dibujar un torso y cabeza básicos como placeholder (estilo holograma/blueprint)
    draw.ellipse([300, 200, 700, 600], fill=(200, 220, 255, 255)) # Cabeza
    draw.rectangle([350, 600, 650, 1024], fill=(150, 180, 220, 255)) # Torso
    body.save(os.path.join(assets_dir, "body.png"))
    
    hair = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_hair = ImageDraw.Draw(hair)
    draw_hair.ellipse([280, 180, 720, 400], fill=(200, 100, 50, 255)) # Pelo pelirrojo
    hair.save(os.path.join(assets_dir, "hair.png"))
    
    # 2. Ojos
    def draw_eye(d, style):
        if style == 'forward':
            d.ellipse([400, 350, 460, 410], fill=(255, 255, 255, 255))
            d.ellipse([540, 350, 600, 410], fill=(255, 255, 255, 255))
            d.ellipse([420, 370, 440, 390], fill=(0, 0, 0, 255)) # pupila
            d.ellipse([560, 370, 580, 390], fill=(0, 0, 0, 255))
        elif style == 'screen':
            d.ellipse([400, 350, 460, 410], fill=(255, 255, 255, 255))
            d.ellipse([540, 350, 600, 410], fill=(255, 255, 255, 255))
            d.ellipse([430, 380, 450, 400], fill=(0, 0, 0, 255)) # pupila abajo
            d.ellipse([570, 380, 590, 400], fill=(0, 0, 0, 255))
        elif style == 'blink':
            d.line([400, 380, 460, 380], fill=(0, 0, 0, 255), width=4)
            d.line([540, 380, 600, 380], fill=(0, 0, 0, 255), width=4)
            
    for eye_style in ['forward', 'screen', 'blink']:
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_eye(ImageDraw.Draw(img), eye_style)
        img.save(os.path.join(eyes_dir, f"eyes_{eye_style}.png"))

    # 3. Manos (Tipeando)
    for i in range(1, 4):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        offset = i * 15
        d.ellipse([400, 700 + offset, 450, 750 + offset], fill=(255, 200, 180, 255))
        d.ellipse([550, 730 - offset, 600, 780 - offset], fill=(255, 200, 180, 255))
        img.save(os.path.join(hands_dir, f"hands_type_{i}.png"))

    # 4. Bocas (Visemas)
    mouth_shapes = {
        'X': lambda d: d.line([460, 500, 540, 500], fill=(0, 0, 0, 255), width=4), # cerrada
        'A': lambda d: d.ellipse([450, 490, 550, 510], fill=(200, 50, 50, 255)),   # MBP
        'B': lambda d: d.rectangle([450, 495, 550, 505], fill=(50, 0, 0, 255)),    # KST
        'C': lambda d: d.ellipse([460, 480, 540, 520], fill=(100, 0, 0, 255)),     # E
        'D': lambda d: d.ellipse([460, 470, 540, 530], fill=(150, 0, 0, 255)),     # A
        'E': lambda d: d.ellipse([470, 485, 530, 515], fill=(100, 0, 0, 255)),     # O
        'F': lambda d: d.ellipse([480, 490, 520, 510], fill=(100, 0, 0, 255)),     # U
    }
    
    for shape, draw_func in mouth_shapes.items():
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_func(ImageDraw.Draw(img))
        img.save(os.path.join(mouth_dir, f"mouth_{shape}.png"))

    print("¡Imágenes de personaje generadas y guardadas en la carpeta 'assets'!")

if __name__ == "__main__":
    setup_assets()
