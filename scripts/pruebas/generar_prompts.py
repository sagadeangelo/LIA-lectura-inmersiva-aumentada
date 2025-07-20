import torch
import json
import sys
from pathlib import Path
from diffusers import StableDiffusionPipeline
from transformers import CLIPTokenizer
from compel import Compel
from PIL import Image

# 📥 Argumentos: escena y archivo de configuración
nombre_escena = sys.argv[1] if len(sys.argv) > 1 else "escena"
archivo_config = sys.argv[2] if len(sys.argv) > 2 else "config_realista.json"
prompt_path = Path("prompt_temp.txt")

# 📖 Cargar configuración del modelo
with open(Path("modelos/configs") / archivo_config, "r", encoding="utf-8") as f:
    config = json.load(f)

modelo_base = config["modelo_base"]
ruta_modelo_base = config["ruta_modelo_base"]
negative_prompt = config["negative_prompt"]
lora_list = config.get("lora", [])

# 🧠 Leer prompt y truncar a 77 tokens
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read().strip()

tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
prompt_tokens = tokenizer(prompt, truncation=True, max_length=77, return_tensors="pt")
prompt = tokenizer.decode(prompt_tokens["input_ids"][0], skip_special_tokens=True)

# 🚀 Cargar modelo base
pipe = StableDiffusionPipeline.from_single_file(
    ruta_modelo_base,
    torch_dtype=torch.float32,
    safety_checker=None
).to("cuda")

# ⚠️ Activar xformers si está disponible
try:
    pipe.enable_xformers_memory_efficient_attention()
except:
    print("⚠️ Xformers no disponible o no compatible, se continuará sin él.")

# 🧩 Aplicar LoRAs si vienen en la configuración
for lora in lora_list:
    nombre = lora["nombre"]
    ruta = lora["ruta"]
    peso = lora.get("peso", 1.0)
    try:
        pipe.load_lora_weights(ruta)
        pipe.fuse_lora(lora_scale=peso)
        print(f"✅ LoRA '{nombre}' cargado con peso {peso}")
    except Exception as e:
        print(f"❌ Error al cargar LoRA '{nombre}': {e}")

# 💬 Convertir texto a embeddings
compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)
prompt_embeds = compel(prompt)
negative_embeds = compel(negative_prompt)

# 🎨 Generar imagen
try:
    image = pipe(
        prompt_embeds=prompt_embeds,
        negative_prompt_embeds=negative_embeds,
        num_inference_steps=20,
        guidance_scale=7.5,
        height=512,
        width=512,
        added_cond_kwargs={}
    ).images[0]

    # 💾 Guardar resultado
    output_path = Path("salida_ia") / f"{nombre_escena}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    print(f"✅ Imagen guardada en: {output_path}")

except Exception as e:
    print(f"❌ Error al generar la imagen: {e}")
