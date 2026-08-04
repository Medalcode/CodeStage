import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from unir_videos import build_concat_list, concat_videos

def test_build_concat_list_non_existent_dir(tmp_path):
    result = build_concat_list(output_dir=tmp_path / "does_not_exist", list_file=tmp_path / "list.txt")
    assert result is False

def test_build_concat_list_no_mp4_files(tmp_path):
    out_dir = tmp_path / "resultados"
    out_dir.mkdir()
    (out_dir / "audio.wav").write_text("dummy audio")
    
    result = build_concat_list(output_dir=out_dir, list_file=tmp_path / "list.txt")
    assert result is False

def test_build_concat_list_success(tmp_path):
    out_dir = tmp_path / "resultados"
    out_dir.mkdir()
    clip1 = out_dir / "clip_001.mp4"
    clip2 = out_dir / "clip_002.mp4"
    clip1.write_text("dummy mp4 1")
    clip2.write_text("dummy mp4 2")
    
    list_file = tmp_path / "lista_temporal.txt"
    result = build_concat_list(output_dir=out_dir, list_file=list_file)
    
    assert result is True
    assert list_file.exists()
    content = list_file.read_text(encoding="utf-8")
    assert "clip_001.mp4" in content
    assert "clip_002.mp4" in content

@patch("shutil.which", return_value="/usr/bin/ffmpeg")
@patch("subprocess.run")
def test_concat_videos_success(mock_run, mock_which, tmp_path):
    list_file = tmp_path / "lista.txt"
    list_file.write_text("file 'clip.mp4'\n")
    final_video = tmp_path / "video_completo.mp4"
    
    mock_run.return_value = MagicMock(returncode=0)
    
    result = concat_videos(list_file=str(list_file), final_video=str(final_video))
    assert result is True
    # Verify temporal list file was cleaned up in try...finally
    assert not list_file.exists()

@patch("shutil.which", return_value=None)
def test_concat_videos_missing_ffmpeg(mock_which, tmp_path):
    list_file = tmp_path / "lista.txt"
    result = concat_videos(list_file=str(list_file), final_video=tmp_path / "video.mp4")
    assert result is False
