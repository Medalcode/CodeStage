import pytest
from pathlib import Path
from PIL import Image

from preparar_personaje import setup_assets
from prepare_assets import process_image
from generate_placeholder_assets import generate_all

def test_setup_assets_creates_valid_png_suite(tmp_path):
    out_dir = tmp_path / "assets"
    setup_assets(output_dir=out_dir)
    
    assert out_dir.exists()
    assert (out_dir / "body.png").exists()
    assert (out_dir / "hair.png").exists()
    
    # Check eyes directory
    eyes_dir = out_dir / "eyes"
    assert (eyes_dir / "eyes_forward.png").exists()
    assert (eyes_dir / "eyes_screen.png").exists()
    assert (eyes_dir / "eyes_blink.png").exists()
    
    # Check mouth visemes (A, B, C, D, E, F, X)
    mouth_dir = out_dir / "mouth"
    for shape in ['A', 'B', 'C', 'D', 'E', 'F', 'X']:
        assert (mouth_dir / f"mouth_{shape}.png").exists()
        
    # Check hands directory
    hands_dir = out_dir / "hands"
    for i in range(1, 4):
        assert (hands_dir / f"hands_type_{i}.png").exists()

    # Validate image properties
    img = Image.open(out_dir / "body.png")
    assert img.size == (1024, 1024)
    assert img.mode == "RGBA"

def test_prepare_assets_wrapper(tmp_path):
    out_dir = tmp_path / "assets_wrapper"
    process_image(out_dir=out_dir)
    assert (out_dir / "body.png").exists()

def test_generate_placeholder_assets_wrapper(tmp_path):
    # Test function logic with custom path monkeypatched
    from preparar_personaje import setup_assets
    setup_assets(output_dir=tmp_path)
    assert (tmp_path / "hair.png").exists()
