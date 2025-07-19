import os
import torch
from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline

# Cargar .env
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
assert HF_TOKEN, "❌ Pon tu HUGGINGFACE_TOKEN en .env"

# Modelo de imagen
model_img = "CompVis/stable-diffusion-v1-4"

# Configuración de dispositivo
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Usando:", device, torch.cuda.get_device_name(0) if device == "cuda" else "CPU")

# Cargar Stable Diffusion 1.4 en FP32
print("🖼️ Cargando Stable Diffusion v1-4...")
pipe = StableDiffusionPipeline.from_pretrained(
    model_img,
    torch_dtype=torch.float32,  # Usar FP32 para mejor calidad
    use_auth_token=HF_TOKEN,
).to(device)
pipe.enable_attention_slicing()  # Fragmentación de atención para optimizar memoria

# Prompt de prueba de alta calidad
prompt = "A surreal futuristic city at sunset, with neon lights glowing on towering skyscrapers, flying cars, and people walking on elevated walkways, surrounded by a misty atmosphere. The sky is a blend of purple, pink, and orange hues, casting a soft glow on the buildings. The streets are bustling with activity, and the scene exudes a sense of vibrant, high-tech energy. Hyper-realistic, highly detailed, cinematic style."

# Función para generar la imagen
def gen_image(prompt, out="test_image.png"):
    try:
        with torch.no_grad():  # Evitar cálculo de gradientes para la imagen
            # Generación de la imagen con alta calidad
            img = pipe(prompt, guidance_scale=15.0, num_inference_steps=50, height=512, width=512).images[0]
            img.save(out)
            print("Imagen guardada:", out)
    except Exception as e:
        print(f"Error al generar la imagen: {e}")
    finally:
        torch.cuda.empty_cache()  # Liberar memoria de la GPU después de la operación

# Ejecutar la generación de imagen
if __name__ == "__main__":
    gen_image(prompt)
