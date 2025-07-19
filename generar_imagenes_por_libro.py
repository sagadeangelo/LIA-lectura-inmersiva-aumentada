import os
import sys
import json
from pathlib import Path
from diffusers import StableDiffusionPipeline
from transformers import CLIPTokenizer
from compel import Compel
from PIL import Image
import torch

# 📁 Ruta del libro
libro_id = sys.argv[1] if len(sys.argv) > 1 else "angelo_artefactos"
ruta_libro = Path("libros") / libro_id

# 📄 Cargar configuración del libro
config_path = ruta_libro / "config_generacion.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

modelo_path = config["ruta_modelo_base"]
negative_prompt = config["negative_prompt"]
lora_activos = config.get("lora", [])

# 🧠 Preparar pipeline
pipe = StableDiffusionPipeline.from_single_file(
    modelo_path,
    torch_dtype=torch.float32,
    safety_checker=None
).to("cuda")

try:
    pipe.enable_xformers_memory_efficient_attention()
except:
    print("⚠️ Xformers no disponible o no compatible.")

# 📦 Preparar Compel para los embeddings
compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)

# 📂 Crear carpeta de salida
salida = ruta_libro / "imagenes"
salida.mkdir(parents=True, exist_ok=True)

# 📂 Recorrer prompts
prompts_dir = ruta_libro / "prompts"
for prompt_file in sorted(prompts_dir.glob("*.txt")):
    nombre_escena = prompt_file.stem
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    prompt_embeds = compel(prompt)
    negative_embeds = compel(negative_prompt)

    try:
        image = pipe(
            prompt_embeds=prompt_embeds,
            negative_prompt_embeds=negative_embeds,
            num_inference_steps=25,
            guidance_scale=7.5,
            height=768,
            width=512
        ).images[0]

        output_path = salida / f"{nombre_escena}.png"
        image.save(output_path)
        print(f"✅ Imagen generada: {output_path.name}")

    except Exception as e:
        print(f"❌ Error con {prompt_file.name}: {e}")
