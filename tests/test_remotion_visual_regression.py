import os
import sys
import shutil
import subprocess
from pathlib import Path
import pytest

REMOTION_DIR = Path(__file__).parent.parent / "remotion-app"

@pytest.mark.skipif(shutil.which("npx") is None and shutil.which("npx.cmd") is None, reason="npx no está instalado")
def test_remotion_visual_regression_169_and_916(tmp_path):
    """
    Prueba de regresión visual que compila fotogramas estáticos 16:9 y 9:16 Shorts en Remotion.
    """
    out_169 = tmp_path / "test_169.png"
    out_916 = tmp_path / "test_916.png"

    npx_cmd = "npx.cmd" if sys.platform.startswith("win") else "npx"

    # 1. Test 16:9 Landscape Frame
    cmd_169 = [npx_cmd, "remotion", "still", "ExpressApiVideo", str(out_169)]
    res_169 = subprocess.run(cmd_169, cwd=str(REMOTION_DIR), capture_output=True, text=True)
    assert res_169.returncode == 0, f"Error renderizando 16:9: {res_169.stderr}"
    assert out_169.exists()
    assert out_169.stat().st_size > 1000

    # 2. Test 9:16 Vertical Shorts Frame
    cmd_916 = [npx_cmd, "remotion", "still", "ExpressApiVideoShorts", str(out_916)]
    res_916 = subprocess.run(cmd_916, cwd=str(REMOTION_DIR), capture_output=True, text=True)
    assert res_916.returncode == 0, f"Error renderizando 9:16 Shorts: {res_916.stderr}"
    assert out_916.exists()
    assert out_916.stat().st_size > 1000
