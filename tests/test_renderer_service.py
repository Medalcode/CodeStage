import pytest
import time
from pathlib import Path
from services.renderer import RemotionRendererService

def test_renderer_service_initialization(tmp_path):
    remotion_dir = tmp_path / "remotion-app"
    output_dir = tmp_path / "output_videos"
    service = RemotionRendererService(remotion_dir=remotion_dir, output_dir=output_dir)

    assert service.status["status"] == "idle"
    assert service.status["progress"] == 0
    assert output_dir.exists()

def test_renderer_service_cleanup_old_temp_files(tmp_path):
    remotion_dir = tmp_path / "remotion-app"
    remotion_dir.mkdir(parents=True, exist_ok=True)
    output_dir = tmp_path / "output_videos"

    service = RemotionRendererService(remotion_dir=remotion_dir, output_dir=output_dir)

    # Create dummy temp file and set mtime to 48 hours ago
    old_temp = remotion_dir / "old_test.tmp"
    old_temp.write_text("old temp data")

    # Set mtime to 2 days ago
    two_days_ago = time.time() - (48 * 3600)
    import os
    os.utime(old_temp, (two_days_ago, two_days_ago))

    cleaned = service.cleanup_old_temp_files(max_age_seconds=86400)
    assert cleaned == 1
    assert not old_temp.exists()
