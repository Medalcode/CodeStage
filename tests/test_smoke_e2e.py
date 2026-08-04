import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from download_rhubarb import download_rhubarb

@patch("urllib.request.urlopen")
@patch("urllib.request.urlretrieve")
@patch("zipfile.ZipFile")
def test_download_rhubarb_smoke(mock_zip, mock_retrieve, mock_urlopen, tmp_path):
    # Mock GitHub API JSON response
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"assets": [{"name": "rhubarb-1.14.0-win.zip", "browser_download_url": "https://github.com/dummy.zip"}]}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    out_dir = tmp_path / "rhubarb"
    download_rhubarb(dest_dir=out_dir)
    
    mock_retrieve.assert_called_once()
    mock_zip.assert_called_once()

def test_full_pipeline_smoke_e2e(tmp_path):
    """
    Smoke E2E test verifying end-to-end flow from guion.txt to assets and mock pipeline execution.
    """
    from utils import split_script
    from preparar_personaje import setup_assets
    
    guion = tmp_path / "guion.txt"
    guion.write_text("Primer párrafo del tutorial.\n\nSegundo párrafo del tutorial.", encoding="utf-8")
    
    chunks = split_script(guion)
    assert len(chunks) == 2
    
    assets_dir = tmp_path / "assets"
    setup_assets(output_dir=assets_dir)
    assert (assets_dir / "body.png").exists()
