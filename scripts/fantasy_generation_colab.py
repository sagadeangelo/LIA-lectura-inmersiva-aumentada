
# 🧙‍♂️ Estilo Fantasía con LoRA Europea/Norteamericana
# Notebook para generación de imágenes IA desde texto usando Stable Diffusion

# ⬇️ Clonar repositorio del proyecto
!rm -rf LIA-lectura-inmersiva-aumentada
!git clone https://github.com/sagadeangelo/LIA-lectura-inmersiva-aumentada.git
%cd LIA-lectura-inmersiva-aumentada

# 🛠️ Instalar dependencias necesarias
!pip install -q diffusers transformers accelerate compel safetensors
!pip install -q git+https://github.com/huggingface/peft.git
!pip install -q xformers

# 🔧 Cargar librerías
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from compel import Compel
from peft import PeftModel
from PIL import Image
import os, uuid, json
from datetime import datetime

# 📁 Crear carpeta para modelos si no existe
os.makedirs("modelos/realistas", exist_ok=True)

# 📥 Descargar modelo de fantasía compatible
!curl -Lo modelos/realistas/revAnimatedFantasy_v2.safetensors https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/revAnimated_v122.safetensors

# 📥 Descargar LoRA europea/norteamericana (Ejemplo funcional)
!curl -Lo modelos/realistas/euro_lora.safetensors https://huggingface.co/NoCrypt/mixReal-Lora/resolve/main/mixReal_v10_euro.safetensors

# ⚙️ Configuración de generación
config = {
    "modelo_base": "revAnimatedFantasy_v2.safetensors",
    "ruta_modelo_base": "modelos/realistas/revAnimatedFantasy_v2.safetensors",
    "lora": [
        {
            "nombre": "euro_lora",
            "archivo": "modelos/realistas/euro_lora.safetensors",
            "peso": 0.8
        }
    ],
    "negative_prompt": "anime, blurry, bad anatomy, deformed, fused fingers, extra limbs, disfigured, low quality, cloned face, bad hands, unrealistic, poorly drawn"
}
with open("libros/config_generacion.json", "w") as f:
    json.dump(config, f, indent=2)

# 🧠 Cargar modelo base
base_model_path = config["ruta_modelo_base"]
pipe = StableDiffusionPipeline.from_single_file(
    base_model_path,
    torch_dtype=torch.float16,
    safety_checker=None,
    requires_safety_checker=False
).to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# 🧩 Tokenizer + Text Encoder para Compel
compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)

# 🪄 Aplicar LoRA
loras = config.get("lora", [])
unet = pipe.unet
for lora in loras:
    ruta_lora = lora.get("archivo")
    if ruta_lora:
        try:
            lora_model = PeftModel.from_pretrained(unet, ruta_lora)
            unet = lora_model.merge_and_unload()
            unet.to("cuda")
            print(f"✅ LoRA aplicado: {ruta_lora}")
        except Exception as e:
            print(f"❌ Error aplicando LoRA '{ruta_lora}': {e}")
pipe.unet = unet

# ✨ Función de generación
def generar_imagen(prompt, output_path="fantasia.png"):
    prompt_compel = compel(prompt)
    image = pipe(prompt_compel, height=1024, width=1024).images[0]
    image.save(output_path)
    display(image)

# ▶️ Prueba de generación
generar_imagen("A majestic wizard riding a glowing eagle through the stormy skies, epic fantasy scene, cinematic lighting, concept art")
