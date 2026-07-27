import os
from PIL import Image, ImageDraw, ImageFont

def create_dirs():
    os.makedirs('assets/mouth', exist_ok=True)
    os.makedirs('assets/eyes', exist_ok=True)
    os.makedirs('assets/hands', exist_ok=True)

def draw_transparent_png(filename, size=(1024, 1024), draw_func=None):
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    if draw_func:
        draw = ImageDraw.Draw(img)
        draw_func(draw)
    img.save(filename)

def make_body():
    def draw(d):
        # Draw torso and laptop
        d.rectangle([300, 500, 700, 1024], fill=(200, 200, 200, 255)) # body
        d.rectangle([100, 700, 900, 1024], fill=(100, 100, 100, 255)) # desk
        d.rectangle([400, 600, 800, 900], fill=(50, 50, 50, 255)) # laptop
    draw_transparent_png('assets/body.png', draw_func=draw)

def make_hair():
    def draw(d):
        # Draw hair
        d.ellipse([300, 100, 700, 550], fill=(100, 50, 20, 255))
        # Face cutout
        d.ellipse([350, 200, 650, 500], fill=(255, 220, 200, 255))
    draw_transparent_png('assets/hair.png', draw_func=draw)

def make_eyes():
    def d_forward(d):
        d.ellipse([420, 300, 480, 360], fill=(255,255,255,255))
        d.ellipse([520, 300, 580, 360], fill=(255,255,255,255))
        d.ellipse([440, 320, 460, 340], fill=(0,0,0,255))
        d.ellipse([540, 320, 560, 340], fill=(0,0,0,255))
    draw_transparent_png('assets/eyes/eyes_forward.png', draw_func=d_forward)
    
    def d_screen(d):
        d.ellipse([420, 300, 480, 360], fill=(255,255,255,255))
        d.ellipse([520, 300, 580, 360], fill=(255,255,255,255))
        d.ellipse([460, 330, 480, 350], fill=(0,0,0,255)) # looking down-right at screen
        d.ellipse([560, 330, 580, 350], fill=(0,0,0,255))
    draw_transparent_png('assets/eyes/eyes_screen.png', draw_func=d_screen)
    
    def d_blink(d):
        d.line([420, 330, 480, 330], fill=(0,0,0,255), width=4)
        d.line([520, 330, 580, 330], fill=(0,0,0,255), width=4)
    draw_transparent_png('assets/eyes/eyes_blink.png', draw_func=d_blink)

def make_mouths():
    # A, B, C, D, E, F, X
    shapes = {
        'X': lambda d: d.line([480, 420, 520, 420], fill=(0,0,0,255), width=3), # closed
        'A': lambda d: d.ellipse([470, 415, 530, 425], fill=(200,50,50,255)), # MBP
        'B': lambda d: d.rectangle([470, 415, 530, 425], fill=(50,0,0,255)), # KST
        'C': lambda d: d.ellipse([470, 410, 530, 430], fill=(100,0,0,255)), # E
        'D': lambda d: d.ellipse([470, 400, 530, 440], fill=(150,0,0,255)), # A open
        'E': lambda d: d.ellipse([480, 405, 520, 435], fill=(100,0,0,255)), # O
        'F': lambda d: d.ellipse([490, 410, 510, 430], fill=(100,0,0,255)), # U
    }
    for name, func in shapes.items():
        draw_transparent_png(f'assets/mouth/mouth_{name}.png', draw_func=func)

def make_hands():
    def h1(d):
        d.ellipse([450, 700, 500, 750], fill=(255, 220, 200, 255))
        d.ellipse([600, 720, 650, 770], fill=(255, 220, 200, 255))
    def h2(d):
        d.ellipse([450, 720, 500, 770], fill=(255, 220, 200, 255))
        d.ellipse([600, 700, 650, 750], fill=(255, 220, 200, 255))
    def h3(d):
        d.ellipse([470, 710, 520, 760], fill=(255, 220, 200, 255))
        d.ellipse([580, 710, 630, 760], fill=(255, 220, 200, 255))
        
    draw_transparent_png('assets/hands/hands_type_1.png', draw_func=h1)
    draw_transparent_png('assets/hands/hands_type_2.png', draw_func=h2)
    draw_transparent_png('assets/hands/hands_type_3.png', draw_func=h3)

if __name__ == "__main__":
    create_dirs()
    make_body()
    make_hair()
    make_eyes()
    make_mouths()
    make_hands()
    print("Assets generados.")
