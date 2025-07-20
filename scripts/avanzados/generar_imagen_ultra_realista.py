# generar_imagen_ultra_realista.py
import torch, os
from diffusers import StableDiffusionXLPipeline
from compel import Compel
from PIL import Image
import json

# === CONFIGURACIÓN ===
ruta_config = "modelos/configs/config_realista_hypervae_lora.json"  # o el estilo que desees

# Cargar configuración JSON
with open(ruta_config, "r", encoding="utf-8") as f:
    config = json.load(f)

modelo_base = config["modelo_base"]
pesos_custom = config["modelo_pesos"]
prompt_negativo = config["prompt_negativo"]
lora = config.get("lora", None)
vae = config.get("vae", None)

# Seleccionar dispositivo
device = "cuda" if torch.cuda.is_available() else "cpu"

# === CARGAR PIPELINE ===
pipe = StableDiffusionXLPipeline.from_pretrained(
    modelo_base,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
    safety_checker=None
).to(device)

# Cargar pesos personalizados
if pesos_custom:
    from safetensors.torch import load_file
    state_dict = load_file(pesos_custom)
    pipe.unet.load_state_dict(state_dict, strict=False)

# Cargar LoRA si aplica
if lora:
    pipe.load_lora_weights(lora)
    pipe.fuse_lora()

# Cargar VAE si aplica
if vae:
    pipe.vae.load_state_dict(load_file(vae))

# Compositor de prompt con Compel
compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder, truncate_long_prompts=True)

# === PROMPT Y PARÁMETROS ===
prompt_usuario = "Retrato heroico realista de un joven guerrero con chaqueta negra, cicatriz en el rostro, fondo oscuro suave, iluminación Rembrandt"
prompt = compel(prompt_usuario)
prompt_neg = compel(prompt_negativo)

# === GENERACIÓN ===
image = pipe(
    prompt_embeds=prompt,
    negative_prompt_embeds=prompt_neg,
    num_inference_steps=40,
    guidance_scale=8.0,
    height=1024,
    width=768
).images[0]

# === GUARDADO ===
os.makedirs("ultra_realistas", exist_ok=True)
output_path = "ultra_realistas/retrato.png"
image.save(output_path)
print(f"✅ Imagen guardada en: {output_path}")
