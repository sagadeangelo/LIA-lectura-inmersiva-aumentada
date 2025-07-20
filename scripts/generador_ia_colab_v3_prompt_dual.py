import os
import uuid
import requests
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# ===============================
# 🔐 Claves API (rellenar aquí o usar .env)
# ===============================
os.environ["FREESOUND_API_KEY"] = "tu_clave_freesound_aqui"
os.environ["HUGGINGFACE_TOKEN"] = "tu_token_huggingface_aqui"

# ===============================
# 🔧 Cargar claves y modelo IA
# ===============================
load_dotenv()
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY", os.environ.get("FREESOUND_API_KEY"))
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", os.environ.get("HUGGINGFACE_TOKEN"))

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    use_auth_token=HUGGINGFACE_TOKEN,
    torch_dtype=torch.float16
).to("cuda")

# ===============================
# 🔊 Funciones para sonido
# ===============================
def buscar_sonido_freesound(prompt):
    headers = {"Authorization": f"Token {FREESOUND_API_KEY}"}
    params = {"query": prompt, "fields": "previews", "filter": "duration:[1.0 TO 15.0]"}
    resp = requests.get("https://freesound.org/apiv2/search/text/", headers=headers, params=params)
    if resp.status_code == 200 and resp.json()["results"]:
        return resp.json()["results"][0]["previews"]["preview-hq-mp3"]
    return None

def extraer_keywords_freesound(texto):
    stopwords = set("el la los las de del con un una en y por para sobre desde junto al a ante bajo durante entre hacia hasta según sin tras".split())
    palabras = texto.lower().split()
    keywords = [p for p in palabras if p.isalpha() and p not in stopwords and len(p) > 3]
    return " ".join(keywords[:3]) if keywords else texto

def generar_nombre_base():
    ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:6]
    return f"{ahora}_{uid}"

# ===============================
# 🧩 Procesar libro
# ===============================
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
        prompt_imagen = linea
        prompt_sonido = extraer_keywords_freesound(linea)
        nombre_base = generar_nombre_base()

        print(f"\n🧩 [{idx+1}/{len(lineas)}] Escena:")
        print(f"🎨 Prompt imagen: {prompt_imagen}")
        print(f"🔊 Prompt sonido: {prompt_sonido}")

        with open(os.path.join(ruta_txt_out, f"{nombre_base}.txt"), "w", encoding="utf-8") as out:
            out.write(linea)

        try:
            img = pipe(prompt_imagen).images[0]
            img.save(os.path.join(ruta_img, f"{nombre_base}.png"))
            print("✅ Imagen generada.")
        except Exception as e:
            print(f"❌ Error generando imagen: {e}")

        sonido_url = buscar_sonido_freesound(prompt_sonido)
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

# ===============================
# 📘 Ejecutar desde Colab
# ===============================
procesar_libro("libros/angelo_ditox/angelo_ditox.txt", "libros/angelo_ditox/escenas_colab")