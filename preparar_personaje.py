import os
from pathlib import Path
from PIL import Image, ImageDraw

def setup_assets(output_dir="assets", width=1024, height=1024):
    """
    Genera la suite completa de sprites 2D transparentes (PNG) requeridos
    para la composición del avatar en compositor.py.
    """
    base_dir = Path(output_dir).resolve()
    mouth_dir = base_dir / "mouth"
    eyes_dir = base_dir / "eyes"
    hands_dir = base_dir / "hands"
    
    mouth_dir.mkdir(parents=True, exist_ok=True)
    eyes_dir.mkdir(parents=True, exist_ok=True)
    hands_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Cuerpo (Body) y Pelo
    body = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_body = ImageDraw.Draw(body)
    draw_body.ellipse([300, 200, 700, 600], fill=(200, 220, 255, 255))   # Cabeza base
    draw_body.rectangle([350, 600, 650, 1024], fill=(150, 180, 220, 255)) # Torso
    draw_body.rectangle([100, 800, 900, 1024], fill=(80, 90, 110, 255))   # Escritorio
    body.save(base_dir / "body.png")
    
    hair = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_hair = ImageDraw.Draw(hair)
    draw_hair.ellipse([280, 180, 720, 400], fill=(200, 100, 50, 255))    # Cabello
    hair.save(base_dir / "hair.png")
    
    # 2. Ojos (Mirada frente, pantalla, parpadeo)
    def draw_eye(d, style):
        if style == 'forward':
            d.ellipse([400, 350, 460, 410], fill=(255, 255, 255, 255))
            d.ellipse([540, 350, 600, 410], fill=(255, 255, 255, 255))
            d.ellipse([420, 370, 440, 390], fill=(0, 0, 0, 255))
            d.ellipse([560, 370, 580, 390], fill=(0, 0, 0, 255))
        elif style == 'screen':
            d.ellipse([400, 350, 460, 410], fill=(255, 255, 255, 255))
            d.ellipse([540, 350, 600, 410], fill=(255, 255, 255, 255))
            d.ellipse([430, 380, 450, 400], fill=(0, 0, 0, 255))
            d.ellipse([570, 380, 590, 400], fill=(0, 0, 0, 255))
        elif style == 'blink':
            d.line([400, 380, 460, 380], fill=(0, 0, 0, 255), width=4)
            d.line([540, 380, 600, 380], fill=(0, 0, 0, 255), width=4)
            
    for eye_style in ['forward', 'screen', 'blink']:
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_eye(ImageDraw.Draw(img), eye_style)
        img.save(eyes_dir / f"eyes_{eye_style}.png")

    # 3. Manos (Tipeando)
    for i in range(1, 4):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        offset = i * 15
        d.ellipse([400, 700 + offset, 450, 750 + offset], fill=(255, 200, 180, 255))
        d.ellipse([550, 730 - offset, 600, 780 - offset], fill=(255, 200, 180, 255))
        img.save(hands_dir / f"hands_type_{i}.png")

    # 4. Bocas (Visemas de Rhubarb: A, B, C, D, E, F, X)
    mouth_shapes = {
        'X': lambda d: d.line([460, 500, 540, 500], fill=(0, 0, 0, 255), width=4),
        'A': lambda d: d.ellipse([450, 490, 550, 510], fill=(200, 50, 50, 255)),
        'B': lambda d: d.rectangle([450, 495, 550, 505], fill=(50, 0, 0, 255)),
        'C': lambda d: d.ellipse([460, 480, 540, 520], fill=(100, 0, 0, 255)),
        'D': lambda d: d.ellipse([460, 470, 540, 530], fill=(150, 0, 0, 255)),
        'E': lambda d: d.ellipse([470, 485, 530, 515], fill=(100, 0, 0, 255)),
        'F': lambda d: d.ellipse([480, 490, 520, 510], fill=(100, 0, 0, 255)),
    }
    
    for shape, draw_func in mouth_shapes.items():
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_func(ImageDraw.Draw(img))
        img.save(mouth_dir / f"mouth_{shape}.png")

    print(f"[+] Assets generados exitosamente en la carpeta '{base_dir}'")

if __name__ == "__main__":
    setup_assets()
