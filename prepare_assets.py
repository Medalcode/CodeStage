import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from PIL import Image, ImageDraw
except ImportError:
    install("Pillow")
    from PIL import Image, ImageDraw

def process_image():
    img_path = r"C:\Users\Jonatthan\.gemini\antigravity\brain\6568efaa-2021-4d7c-98f4-d0f98c57e698\redhead_programmer_girl_1785485393011.jpg"
    out_dir = r"E:\Github\canal-tutorial-automation\assets"
    
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    
    # Body: For the body, we will just use the full image for now
    img.save(os.path.join(out_dir, "body.png"))
    
    # Create empty hair (not needed if body has hair, but required by script)
    empty = Image.new("RGBA", (width, height), (0,0,0,0))
    empty.save(os.path.join(out_dir, "hair.png"))
    
    # Create dummy hands
    empty.save(os.path.join(out_dir, "hands", "hands_type_1.png"))
    empty.save(os.path.join(out_dir, "hands", "hands_type_2.png"))
    empty.save(os.path.join(out_dir, "hands", "hands_type_3.png"))
    
    # We will draw some cartoon mouths over the face.
    # Assuming face is around center. Let's make some simple mouth shapes on transparent bg.
    mouth_dir = os.path.join(out_dir, "mouth")
    eyes_dir = os.path.join(out_dir, "eyes")
    
    shapes = ['A', 'B', 'C', 'D', 'E', 'F', 'X']
    for s in shapes:
        m = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(m)
        cx, cy = width//2, height//2 + 50
        if s == 'X':
            draw.line([cx-20, cy, cx+20, cy], fill=(0,0,0,255), width=3)
        elif s == 'A':
            draw.ellipse([cx-15, cy-5, cx+15, cy+5], fill=(200,50,50,255))
        elif s == 'B':
            draw.rectangle([cx-15, cy-2, cx+15, cy+2], fill=(50,0,0,255))
        elif s == 'C':
            draw.ellipse([cx-15, cy-10, cx+15, cy+10], fill=(100,0,0,255))
        elif s == 'D':
            draw.ellipse([cx-20, cy-15, cx+20, cy+15], fill=(150,0,0,255))
        elif s == 'E':
            draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(100,0,0,255))
        elif s == 'F':
            draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=(100,0,0,255))
        m.save(os.path.join(mouth_dir, f"mouth_{s}.png"))
        
    for e in ['forward', 'screen', 'blink']:
        eye_img = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(eye_img)
        cx1, cy1 = width//2 - 40, height//2 - 30
        cx2, cy2 = width//2 + 40, height//2 - 30
        if e == 'forward':
            draw.ellipse([cx1-5, cy1-5, cx1+5, cy1+5], fill=(0,0,0,255))
            draw.ellipse([cx2-5, cy2-5, cx2+5, cy2+5], fill=(0,0,0,255))
        elif e == 'screen':
            draw.ellipse([cx1-5, cy1+5, cx1+5, cy1+15], fill=(0,0,0,255))
            draw.ellipse([cx2-5, cy2+5, cx2+5, cy2+15], fill=(0,0,0,255))
        elif e == 'blink':
            draw.line([cx1-15, cy1, cx1+15, cy1], fill=(0,0,0,255), width=3)
            draw.line([cx2-15, cy2, cx2+15, cy2], fill=(0,0,0,255), width=3)
        eye_img.save(os.path.join(eyes_dir, f"eyes_{e}.png"))
        
    print("Assets created successfully.")

if __name__ == "__main__":
    import os
    process_image()
