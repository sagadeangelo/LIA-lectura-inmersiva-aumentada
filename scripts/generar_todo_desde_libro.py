import os
import uuid
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# Cargar claves del entorno
load_dotenv()
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Inicializar modelo de imagen
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    use_auth_token=HUGGINGFACE_TOKEN,
    torch_dtype=torch.float16
).to("cuda")

# Buscar sonido en Freesound
def buscar_sonido_freesound(prompt):
    headers = {"Authorization": f"Token {FREESOUND_API_KEY}"}
    params = {"query": prompt, "fields": "previews", "filter": "duration:[1.0 TO 15.0]"}
    resp = requests.get("https://freesound.org/apiv2/search/text/", headers=headers, params=params)

    if resp.status_code == 200:
        data = resp.json()
        if data["results"]:
            return data["results"][0]["previews"]["preview-hq-mp3"]
    return None

# Generar identificador único
def generar_nombre_base():
    ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:6]
    return f"{ahora}_{uid}"

# Procesar cada línea del libro
def procesar_libro(ruta_txt, ruta_salida):
    ruta_img = os.path.join(ruta_salida, "imagenes")
    ruta_snd = os.path.join(ruta_salida, "audios")
    ruta_txt_out = os.path.join(ruta_salida, "textos")
    os.makedirs(ruta_img, exist_ok=True)
    os.makedirs(ruta_snd, exist_ok=True)
    os.makedirs(ruta_txt_out, exist_ok=True)

    with open(ruta_txt, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]

    for idx, linea in enumerate(lineas):
        nombre_base = generar_nombre_base()
        print(f"\n🧩 [{idx+1}/{len(lineas)}] Procesando escena:\n{linea}")

        # Guardar texto original
        with open(os.path.join(ruta_txt_out, f"{nombre_base}.txt"), "w", encoding="utf-8") as out:
            out.write(linea)

        # Generar imagen
        try:
            img = pipe(linea).images[0]
            img.save(os.path.join(ruta_img, f"{nombre_base}.png"))
            print("✅ Imagen generada.")
        except Exception as e:
            print(f"❌ Error generando imagen: {e}")

        # Descargar sonido
        sonido_url = buscar_sonido_freesound(linea)
        if sonido_url:
            try:
                sonido_data = requests.get(sonido_url)
                with open(os.path.join(ruta_snd, f"{nombre_base}.mp3"), "wb") as snd_out:
                    snd_out.write(sonido_data.content)
                print("✅ Sonido descargado.")
            except Exception as e:
                print(f"❌ Error descargando sonido: {e}")
        else:
            print("⚠️ No se encontró sonido.")

# Modo ejecutable desde consola o colab
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--libro", required=True, help="Ruta al archivo de texto del libro")
    parser.add_argument("--ruta", default="escenas", help="Carpeta donde guardar resultados")
    args = parser.parse_args()

    procesar_libro(args.libro, args.ruta)