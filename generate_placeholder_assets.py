from pathlib import Path
from preparar_personaje import setup_assets

def generate_all():
    out_dir = Path(__file__).parent / "assets"
    setup_assets(output_dir=out_dir)

if __name__ == "__main__":
    generate_all()
