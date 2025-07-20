import os
import uuid
import json
import requests
from datetime import datetime
from PIL import Image
from compel import Compel
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, UNet2DConditionModel, AutoencoderKL
from peft import PeftModel
from transformers import CLIPTextModel, CLIPTokenizer
import torch
from dotenv import load_dotenv

# 🔐 Cargar claves
load_dotenv()
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")

# 📘 Rutas
ruta_libro = "libros/angelo_ditox/angelo_ditox.txt"
ruta_config = "libros/angelo_ditox/config_generacion.json"
base_salida = "libros/angelo_ditox"

# 🧠 Cargar configuración del modelo
with open(ruta_config, encoding="utf-8") as f:
    config = json.load(f)

modelo_base = config["ruta_modelo_base"]
negative_prompt = config["negative_prompt"]
loras = config.get("lora", [])

# 🧠 Preparar texto a prompt con compel
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-large-patch14")
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")
unet = UNet2DConditionModel.from_pretrained("runwayml/stable-diffusion-v1-5", subfolder="unet")

# 🪄 Aplicar LoRA si hay
for lora in loras:
    ruta_lora = lora.get("ruta") or lora.get("archivo")
    if ruta_lora:
        try:
            pipe.load_lora_weights(ruta_lora)
            print(f"✅ LoRA aplicado: {ruta_lora}")
        except Exception as e:
            print(f"❌ Error aplicando LoRA '{ruta_lora}': {e}")

    else:
        print("⚠️ LoRA ignorado: no se especificó 'ruta' ni 'archivo'.")


# 🖼️ Crear pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    vae=vae,
    text_encoder=text_encoder,
    tokenizer=tokenizer,
    unet=unet,
    torch_dtype=torch.float16,
    safety_checker=None,
    requires_safety_checker=False
).to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
compel = Compel(tokenizer=tokenizer, text_encoder=text_encoder)

# 🎧 Equivalencias para sonido
EQUIVALENCIAS = {
    "rodar": "rolling wheels on road", "moverse": "footsteps moving",
    "mudarse": "boxes being moved", "viajar": "train ambience",
    "caminar": "footsteps on gravel", "luchar": "sword fight",
    "lluvia": "rain on rooftop", "gritar": "distant scream",
    "pelear": "punching", "susurrar": "whispers",
    "trueno": "thunder rumble", "llorar": "crying",
    "volar": "wind gust", "despertar": "alarm clock",
    "correr": "running steps"
}

# 🔍 Buscar sonido
def buscar_sonido(prompt):
    headers = {"Authorization": f"Token {FREESOUND_API_KEY}"}
    params = {"query": prompt, "fields": "previews", "filter": "duration:[2.0 TO 20.0]"}
    r = requests.get("https://freesound.org/apiv2/search/text/", headers=headers, params=params)
    if r.status_code == 200:
        data = r.json()
        if data["results"]:
            return data["results"][0]["previews"]["preview-hq-mp3"]
    return None

# 🛠 Nombre único
def nombre_unico():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    u = uuid.uuid4().hex[:6]
    return f"{t}_{u}"

# 📚 Procesar libro
def procesar_libro():
    rutas = {
        "imagenes": os.path.join(base_salida, "imagenes"),
        "audios": os.path.join(base_salida, "audios"),
        "escenas": os.path.join(base_salida, "escenas"),
        "prompts": os.path.join(base_salida, "prompts")
    }
    for ruta in rutas.values():
        os.makedirs(ruta, exist_ok=True)

    with open(ruta_libro, encoding="utf-8") as f:
        escenas = [l.strip() for l in f if l.strip()]

    for idx, escena in enumerate(escenas):
        nombre = nombre_unico()
        print(f"\n📖 [{idx+1}/{len(escenas)}] {escena}")

        # Imagen
        prompt_img = escena[:250]
        try:
            emb = compel(prompt_img)
            img = pipe(prompt_embeds=emb, negative_prompt=negative_prompt).images[0]
            img.save(os.path.join(rutas["imagenes"], f"{nombre}.png"))
            print("🖼️ Imagen lista.")
        except Exception as e:
            print(f"⚠️ Error en imagen: {e}")

        # Sonido
        prompt_snd = next((EQUIVALENCIAS[p] for p in escena.lower().split() if p in EQUIVALENCIAS), None)
        if prompt_snd:
            url = buscar_sonido(prompt_snd)
            if url:
                audio = requests.get(url)
                with open(os.path.join(rutas["audios"], f"{nombre}.mp3"), "wb") as f:
                    f.write(audio.content)
                print("🔊 Sonido listo.")
            else:
                print("⚠️ Sin sonido encontrado.")
        else:
            print("⚠️ No hay equivalencia de sonido.")

        # Guardar texto y prompts
        with open(os.path.join(rutas["escenas"], f"{nombre}.txt"), "w", encoding="utf-8") as f:
            f.write(escena)
        with open(os.path.join(rutas["prompts"], f"{nombre}.txt"), "w", encoding="utf-8") as f:
            f.write(f"imagen: {prompt_img}\nsonido: {prompt_snd or 'ninguno'}")

# ▶️ Ejecutar
procesar_libro()
