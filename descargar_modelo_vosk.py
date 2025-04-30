import os, zipfile, wget

url = "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
output_zip = "vosk_model.zip"
ruta_modelos = "models"

print("Descargando modelo VOSK...")
wget.download(url, output_zip)

print("\nDescomprimiendo...")
with zipfile.ZipFile(output_zip, 'r') as zip_ref:
    zip_ref.extractall(ruta_modelos)

os.remove(output_zip)
print("✅ Modelo descargado y extraído en la carpeta 'models/'")
