import urllib.request
import json
import zipfile
import os

api_url = "https://api.github.com/repos/DanielSWolf/rhubarb-lip-sync/releases/latest"
print(f"Fetching {api_url}...")
try:
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
    download_url = None
    for asset in data['assets']:
        if 'win' in asset['name'].lower() and asset['name'].endswith('.zip'):
            download_url = asset['browser_download_url']
            break
            
    if download_url:
        print(f"Downloading {download_url}...")
        zip_path = "rhubarb.zip"
        urllib.request.urlretrieve(download_url, zip_path)
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("rhubarb")
        os.remove(zip_path)
        print("Done.")
    else:
        print("Could not find Windows zip in the latest release.")
except Exception as e:
    print(f"Error: {e}")
