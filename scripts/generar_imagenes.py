# generar_imagen_ia.py
import sys
import os
import torch
from diffusers import StableDiffusionPipeline
from diffusers.utils import load_image
from PIL import Image

# ✅ Comprobar argumentos
if len(sys.argv) < 2:
    print("Uso: python generar_imagen_ia.py [prompt] [nombre_archivo_sin_extension]")
    print("O:   python generar_imagen_ia.py nombre_archivo_sin_extension  (lee el prompt desde prompt_temp.txt)")
    sys.exit(1)

# 🧠 Leer el prompt
if len(sys.argv) == 2:
    nombre_base = sys.argv[1]
    temp_prompt_path = os.path.join(os.path.dirname(__file__), "prompt_temp.txt")
    if not os.path.exists(temp_prompt_path):
        print("❌ No se encontró prompt_temp.txt")
        sys.exit(1)
    with open(temp_prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read().strip()
else:
    prompt = sys.argv[1]
    nombre_base = sys.argv[2]

# 📂 Directorio de salida
salida_dir = os.path.join(os.getcwd(), "salida_ia")
os.makedirs(salida_dir, exist_ok=True)

# 🖼️ Ruta de la imagen de salida
salida_path = os.path.join(salida_dir, f"{nombre_base}.png")

# 🧠 Cargar modelo Realistic Vision
# Ruta absoluta segura del modelo
modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "modelos", "realistas", "realisticVisionV60B1_v51HyperVAE.safetensors"))

if not os.path.exists(modelo_path):
    print(f"❌ No se encontró el modelo en: {modelo_path}")
    sys.exit(1)

pipe = StableDiffusionPipeline.from_single_file(modelo_path, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# 📏 Establecer resolución HD (720x1280)
pipe.scheduler.set_timesteps(50)
generator = torch.manual_seed(42)  # semilla fija para pruebas reproducibles
image = pipe(
    prompt,
    negative_prompt="deformed hands, extra limbs, blurry, watermark, text",
    height=1280,
    width=720,
    generator=generator
).images[0]


# 💾 Guardar
image.save(salida_path)

# ✅ Confirmación
print(f"✅ Imagen generada y guardada en: {salida_path}")
