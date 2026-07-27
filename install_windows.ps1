param (
    [switch]$SkipGitClone = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================="
Write-Host "Instalador de SadTalker para Windows (RTX)"
Write-Host "========================================="

# 1. Clonar SadTalker si no existe
if (-Not $SkipGitClone) {
    if (-Not (Test-Path "SadTalker")) {
        Write-Host "[*] Clonando el repositorio oficial de SadTalker..."
        git clone https://github.com/OpenTalker/SadTalker.git
    } else {
        Write-Host "[*] La carpeta SadTalker ya existe. Omitiendo clone."
    }
}

Set-Location -Path "SadTalker"

# 2. Crear entorno virtual
if (-Not (Test-Path "sadtalker_env")) {
    Write-Host "[*] Creando entorno virtual 'sadtalker_env' usando Python 3.10..."
    py -3.10 -m venv sadtalker_env
} else {
    Write-Host "[*] El entorno virtual ya existe."
}

# 3. Activar el entorno e instalar dependencias
Write-Host "[*] Instalando dependencias (esto puede tomar varios minutos)..."

# Script block para ejecutar comandos dentro del entorno virtual activado
$activateScript = ".\sadtalker_env\Scripts\Activate.ps1"
if (-Not (Test-Path $activateScript)) {
    Write-Host "[!] No se encontró el script de activación. Verifica si Python está instalado correctamente."
    exit
}

# Usamos PowerShell para ejecutar la secuencia de comandos con el entorno activado
& powershell -NoProfile -ExecutionPolicy Bypass -Command "
    . $activateScript
    
    Write-Host '[-] Actualizando pip...'
    python -m pip install --upgrade pip setuptools wheel
    
    Write-Host '[-] Instalando PyTorch con CUDA 12.1...'
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    
    Write-Host '[-] Instalando requerimientos de SadTalker...'
    pip install -r requirements.txt
    
    Write-Host '[-] Instalando edge-tts para generación de voz...'
    pip install edge-tts
    
    Write-Host '[-] Aplicando parche para bug de basicsr...'
    # Corregir el import problemático en basicsr
    `$fileToPatch = '.\sadtalker_env\Lib\site-packages\basicsr\data\degradations.py'
    if (Test-Path `$fileToPatch) {
        (Get-Content `$fileToPatch) -replace 'from torchvision.transforms.functional_tensor import rgb_to_grayscale', 'from torchvision.transforms.functional import rgb_to_grayscale' | Set-Content `$fileToPatch
        Write-Host '[-] Parche aplicado exitosamente.'
    } else {
        Write-Host '[-] Archivo a parchear no encontrado, omitiendo.'
    }
"

# 4. Descargar modelos preentrenados
Write-Host "[*] Descargando modelos preentrenados (GFPGAN, etc.)..."
Write-Host "[*] (Por favor espera, son varios GB...)"
& powershell -NoProfile -ExecutionPolicy Bypass -Command "
    if (Get-Command bash -ErrorAction SilentlyContinue) {
        bash scripts/download_models.sh
    } else {
        Write-Host '[!] No se encontró bash (Git Bash). Por favor, descarga los modelos manualmente.'
        Write-Host '[*] Intentando descargar con un script de python...'
        py -3.10 -c `"
import urllib.request
import os

os.makedirs('checkpoints', exist_ok=True)
models = {
    'mapping_00109-model.pth.tar': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar',
    'mapping_00229-model.pth.tar': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar',
    'SadTalker_V0.0.2_256.safetensors': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors',
    'SadTalker_V0.0.2_512.safetensors': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors'
}

for name, url in models.items():
    dest = os.path.join('checkpoints', name)
    if not os.path.exists(dest):
        print(f'Descargando {name}...')
        urllib.request.urlretrieve(url, dest)

os.makedirs('gfpgan/weights', exist_ok=True)
gfpgan_models = {
    'alignment_WFLW_4HG.pth': 'https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth',
    'detection_Resnet50_Final.pth': 'https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth',
    'GFPGANv1.4.pth': 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth',
    'parsing_parsenet.pth': 'https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth'
}

for name, url in gfpgan_models.items():
    dest = os.path.join('gfpgan/weights', name)
    if not os.path.exists(dest):
        print(f'Descargando {name}...')
        urllib.request.urlretrieve(url, dest)
`"
    }
"

Write-Host "========================================="
Write-Host "[+] Instalación completada."
Write-Host "Para usar el sistema, asegúrate de activar el entorno:"
Write-Host ".\SadTalker\sadtalker_env\Scripts\Activate.ps1"
Write-Host "========================================="
