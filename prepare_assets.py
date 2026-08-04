import os
from pathlib import Path
from preparar_personaje import setup_assets

def process_image(out_dir=None):
    """
    Punto de entrada compatible que genera o actualiza la carpeta de assets
    sin requerir rutas absolutas hardcodeadas en disco.
    """
    if out_dir is None:
        out_dir = Path(__file__).parent / "assets"
    setup_assets(output_dir=out_dir)

if __name__ == "__main__":
    process_image()
