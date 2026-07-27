import urllib.request
import os
import sys

def download_file(url, dest):
    if not os.path.exists(dest):
        print(f"Descargando {os.path.basename(dest)}...")
        urllib.request.urlretrieve(url, dest)
    else:
        print(f"[{os.path.basename(dest)}] ya existe.")

def main():
    os.chdir(os.path.join(os.path.dirname(__file__), "SadTalker"))

    os.makedirs('checkpoints', exist_ok=True)
    models = {
        'mapping_00109-model.pth.tar': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar',
        'mapping_00229-model.pth.tar': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar',
        'SadTalker_V0.0.2_256.safetensors': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors',
        'SadTalker_V0.0.2_512.safetensors': 'https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors'
    }

    for name, url in models.items():
        download_file(url, os.path.join('checkpoints', name))

    os.makedirs('gfpgan/weights', exist_ok=True)
    gfpgan_models = {
        'alignment_WFLW_4HG.pth': 'https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth',
        'detection_Resnet50_Final.pth': 'https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth',
        'GFPGANv1.4.pth': 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth',
        'parsing_parsenet.pth': 'https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth'
    }

    for name, url in gfpgan_models.items():
        download_file(url, os.path.join('gfpgan/weights', name))

    print("Todos los modelos han sido descargados correctamente.")

if __name__ == "__main__":
    main()
