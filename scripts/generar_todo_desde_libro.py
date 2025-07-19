
import os
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv
import requests
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline
from safetensors.torch import load_file
from PIL import Image
import freesound
import re
from compel import Compel

# === CONFIG ===
load_dotenv()
FREESOUND_API_KEY = os.getenv("FREESOUND_ACCESS_TOKEN") or os.getenv("FREESOUND_API_KEY")
if not FREESOUND_API_KEY:
    raise ValueError("FREESOUND_API_KEY no está en .env")

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
modelo_gpt = AutoModelForCausalLM.from_pretrained(
    "EleutherAI/gpt-neo-1.3B",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    low_cpu_mem_usage=True
).to(device)

modelo_base = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    modelo_base,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None,
    variant="fp16" if device == "cuda" else None
).to(device)

compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)

# Pesos personalizados (ajusta si es necesario)
pesos_custom = "modelos/realistas/realisticVisionV60B1_v51HyperVAE.safetensors"
if os.path.exists(pesos_custom):
    print("Cargando pesos personalizados...")
    state_dict = load_file(pesos_custom)
    pipe.unet.load_state_dict(state_dict, strict=False)

# Cliente Freesound
client = freesound.FreesoundClient()
client.set_token(FREESOUND_API_KEY)

def dividir_capitulos_escenas(texto):
    caps = re.split(r"(?=CAP[IÍ]TULO\s+[XVI0-9]+)", texto, flags=re.IGNORECASE)
    resultado = []
    for idx, cap in enumerate(caps):
        if not cap.strip(): continue
        escenas = [e.strip() for e in cap.strip().split("\n\n") if len(e.strip()) > 30]
        resultado.append((f"cap_{idx+1:02d}", escenas))
    return resultado

def generar_prompt(texto):
    entrada = f"Describe visualmente esta escena: {texto}"
    inputs = tokenizer(entrada, return_tensors="pt").to(device)
    output = modelo_gpt.generate(
        **inputs, max_new_tokens=40, do_sample=True, temperature=0.9,
        top_p=0.95, pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

def generar_imagen(prompt, ruta):
    prompt_embeds = compel(prompt)
    img = pipe(prompt_embeds=prompt_embeds, num_inference_steps=30, guidance_scale=7.5).images[0]
    img.save(ruta)

def buscar_audio(texto, ruta_salida):
    query = f"{texto} sound"
    results = client.text_search(query=query, filter="wav", fields="id,name,previews")
    if results["count"] > 0:
        url = results["results"][0]["previews"]["preview-hq-mp3"]
        with requests.get(url, stream=True) as r:
            if r.status_code == 200:
                with open(ruta_salida, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                return True
    return False

def main(libro, ruta_txt):
    base = Path("libros") / libro
    escenas_dir = base / "escenas"
    prompts_dir = base / "prompts"
    imagenes_dir = base / "imagenes"
    audios_dir = base / "audios"
    for d in [escenas_dir, prompts_dir, imagenes_dir, audios_dir]:
        d.mkdir(parents=True, exist_ok=True)

    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    capitulos = dividir_capitulos_escenas(texto)
    total = 0
    for cap_id, escenas in capitulos:
        for i, escena in enumerate(escenas):
            nombre = f"{cap_id}_esc{i+1:02d}"
            ruta_escena = escenas_dir / f"{nombre}.txt"
            ruta_prompt = prompts_dir / f"{nombre}.txt"
            ruta_imagen = imagenes_dir / f"{nombre}.png"
            ruta_audio = audios_dir / f"{nombre}.mp3"

            with open(ruta_escena, "w", encoding="utf-8") as f:
                f.write(escena)

            prompt = generar_prompt(escena)
            with open(ruta_prompt, "w", encoding="utf-8") as f:
                f.write(prompt)

            print(f"🎨 Generando imagen para: {nombre}")
            generar_imagen(prompt, ruta_imagen)

            print(f"🔊 Buscando sonido para: {nombre}")
            if not buscar_audio(escena, ruta_audio):
                print("❌ No se encontró audio.")

            total += 1

    print(f"✔️ Generación completa: {total} escenas procesadas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--libro", required=True, help="Nombre del libro (carpeta)")
    parser.add_argument("--ruta", required=True, help="Ruta al archivo .txt del libro")
    args = parser.parse_args()

    main(args.libro, args.ruta)
