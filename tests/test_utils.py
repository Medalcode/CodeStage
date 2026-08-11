import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from utils import split_script, ensure_dir, get_rhubarb_path, generate_audio, get_audio_hash

def test_split_script_valid_file(tmp_path):
    guion = tmp_path / "guion.txt"
    content = "Hola a todos, bienvenidos.\n\nEn este video aprenderemos Python.\n\n¡Suscríbete al canal!"
    guion.write_text(content, encoding="utf-8")
    
    chunks = split_script(guion)
    assert len(chunks) == 3
    assert chunks[0] == "Hola a todos, bienvenidos."
    assert chunks[1] == "En este video aprenderemos Python."
    assert chunks[2] == "¡Suscríbete al canal!"

def test_split_script_file_not_found():
    with pytest.raises(FileNotFoundError):
        split_script("non_existent_file_12345.txt")

def test_split_script_encoding_latin1(tmp_path):
    guion = tmp_path / "guion_latin1.txt"
    content = "Canción de prueba con acentos en español."
    guion.write_bytes(content.encode("latin-1"))
    
    chunks = split_script(guion)
    assert len(chunks) == 1
    assert "Canción" in chunks[0]

def test_ensure_dir(tmp_path):
    target = tmp_path / "nested" / "dir"
    result = ensure_dir(target)
    assert result.exists()
    assert result.is_dir()

def test_get_audio_hash():
    h1 = get_audio_hash("Hola mundo", "es-MX-DaliaNeural")
    h2 = get_audio_hash("Hola mundo", "es-MX-DaliaNeural")
    h3 = get_audio_hash("Hola mundo diferente", "es-MX-DaliaNeural")
    assert h1 == h2
    assert h1 != h3

def test_get_rhubarb_path_local_fallback(tmp_path):
    rhubarb_dir = tmp_path / "rhubarb"
    rhubarb_dir.mkdir()
    exe = rhubarb_dir / "rhubarb.exe"
    exe.write_text("dummy binary content")
    
    found = get_rhubarb_path(base_dir=tmp_path)
    assert Path(found).resolve() == exe.resolve()

@patch("subprocess.run")
def test_generate_audio_success(mock_run, tmp_path):
    out_file = tmp_path / "audio.wav"
    mock_run.return_value = MagicMock(returncode=0)
    
    result = generate_audio("Hola mundo", out_file, use_cache=False)
    assert result == str(out_file)
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_generate_audio_failure(mock_run, tmp_path):
    import subprocess
    out_file = tmp_path / "audio.wav"
    mock_run.side_effect = subprocess.CalledProcessError(1, "edge-tts", stderr="TTS Network Error")
    
    with pytest.raises(RuntimeError) as exc_info:
        generate_audio("Hola", out_file, use_cache=False)
    assert "Error al generar audio" in str(exc_info.value)
