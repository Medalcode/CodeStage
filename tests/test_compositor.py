import pytest
from pathlib import Path
from preparar_personaje import setup_assets

# Skip if moviepy is not installed in the current environment
moviepy = pytest.importorskip("moviepy")
from compositor import load_avatar_assets

def test_load_avatar_assets_success(tmp_path):
    assets_dir = tmp_path / "assets"
    setup_assets(output_dir=assets_dir)
    
    loaded = load_avatar_assets(assets_dir=assets_dir)
    assert "body" in loaded
    assert "hair" in loaded
    assert "eyes_forward" in loaded
    assert len(loaded["mouths"]) == 7
    assert len(loaded["hands"]) == 3

def test_load_avatar_assets_missing_dir():
    with pytest.raises(FileNotFoundError):
        load_avatar_assets(assets_dir="non_existent_assets_dir_99")
