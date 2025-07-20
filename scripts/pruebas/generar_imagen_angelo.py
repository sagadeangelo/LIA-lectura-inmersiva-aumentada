import os
from dotenv import load_dotenv
import torch
from diffusers import StableDiffusionPipeline

# Cargar variables del archivo .env
load_dotenv()
hf_token = os.getenv("HF_TOKEN")  # Token de Hugging Face desde .env

# Configura las rutas (cámbialas según tu proyecto)
model_path = "ruta/a/tu/modelo_LoRA"       # Ruta a tu modelo LoRA o base
output_folder = "ruta/a/tu/carpeta/salida"  # Carpeta donde guardar la imagen

device = "cuda" if torch.cuda.is_available() else "cpu"

# Cargar el pipeline de Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    revision="fp16",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_auth_token=hf_token
).to(device)

# Prompt descriptivo para Ángelo
prompt = (
    "A heroic character named Ángelo, with short dark hair and intense, piercing eyes. "
    "He wears a modern but mystical outfit, consisting of a leather jacket, a dark shirt, and rugged pants. "
    "His expression is serious yet determined. He has a powerful aura surrounding him, with soft light highlighting his features, "
    "adding a semi-realistic and dramatic effect. He stands in a strong, confident pose, with a subtle glowing light in the background, "
    "giving the scene a mystical and magical atmosphere. The style is semi-realistic, with fine details and soft shading to emphasize the character's features and mood. "
    "The lighting creates a dynamic contrast, highlighting Ángelo's heroic stature."
)

def generar_imagen(prompt_text, output_dir):
    # Generar imagen
    image = pipe(prompt_text).images[0]

    # Crear nombre de archivo basado en el prompt (primeras 8 palabras)
    filename = "_".join(prompt_text.strip().split()[:8]) + ".png"
    output_path = os.path.join(output_dir, filename)

    # Crear carpeta si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Guardar imagen
    image.save(output_path)
    print(f"✅ Imagen guardada en: {output_path}")

if __name__ == "__main__":
    generar_imagen(prompt, output_folder)