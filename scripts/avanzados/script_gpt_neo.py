import os
import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline

# Cargar .env
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
assert HF_TOKEN, "❌ Pon tu HUGGINGFACE_TOKEN en .env"

# Modelos
model_text = "distilgpt2"  # Usamos DistilGPT-2 (82M)
model_img = "CompVis/stable-diffusion-v1-4"

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Usando:", device, torch.cuda.get_device_name(0) if device == "cuda" else "CPU")

# Cargar DistilGPT-2 (82M)
print("🔡 Cargando DistilGPT-2 (82M)...")
tokenizer = AutoTokenizer.from_pretrained(model_text, use_auth_token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_text, use_auth_token=HF_TOKEN).to(device)

# Cargar Stable Diffusion 1.4 en FP32 para optimizar la calidad de la imagen
print("🖼️ Cargando Stable Diffusion v1-4...")
pipe = StableDiffusionPipeline.from_pretrained(
    model_img,
    torch_dtype=torch.float32,  # Usar FP32 en lugar de FP16 para mejor calidad
    use_auth_token=HF_TOKEN,
).to(device)
pipe.enable_attention_slicing()  # Fragmentación de atención para optimizar memoria

# Funciones
def gen_prompt(txt):
    with torch.no_grad():  # Evitar el cálculo de gradientes
        inp = tokenizer(f"Describe cinematográficamente: {txt}", return_tensors="pt").to(device)
        out = model.generate(**inp, max_length=80, do_sample=True, top_p=0.9)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def gen_image(prompt, out="test.png"):
    try:
        with torch.no_grad():  # Evitar el cálculo de gradientes para la imagen
            # Generación de la imagen con resolución reducida y pasos de inferencia reducidos
            img = pipe(prompt, guidance_scale=10.0, num_inference_steps=20, height=256, width=256).images[0]
            img.save(out)
            print("Imagen guardada:", out)
    except Exception as e:
        print(f"Error al generar la imagen: {e}")
    finally:
        torch.cuda.empty_cache()  # Liberar memoria de la GPU después de la operación

if __name__ == "__main__":
    escena = "Una nave abandona la ciudad iluminada por neón"
    prompt = gen_prompt(escena)
    print("🎯 Prompt:", prompt)
    gen_image(prompt)
