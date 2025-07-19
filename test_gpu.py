import torch
from diffusers import StableDiffusionPipeline  # Asegúrate de importar esto

# Verificar si CUDA está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️ Usando dispositivo: {device}")

# Configuración del modelo de Stable Diffusion
model_name_sd = "runwayml/stable-diffusion-v1-5"  # Puedes poner tu modelo aquí
HF_TOKEN = "tu_token_de_huggingface"  # Reemplaza con tu token de Hugging Face

# Cargar el modelo de Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained(
    model_name_sd,
    revision="fp16" if device == "cuda" else None,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_auth_token=HF_TOKEN,
)

# Mover el modelo al dispositivo (GPU o CPU)
pipe = pipe.to(device)

# Verificar que el modelo se cargó correctamente en la GPU
if torch.cuda.is_available():
    print("🌟 GPU detectada y modelo movido a la GPU.")
else:
    print("🚨 No se detectó GPU. El modelo está usando la CPU.")

