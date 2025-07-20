import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline
from safetensors.torch import load_file
from PIL import Image
import freesound
import requests

# === CONFIGURACIÓN ===

# Modelo de texto: GPT-Neo 1.3B (más potente que distilgpt2)
modelo_texto = "EleutherAI/gpt-neo-1.3B"

# Detectar dispositivo GPU si está disponible, si no CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

# Cargar tokenizer y modelo con fp16 para GPU, o float32 para CPU
tokenizer = AutoTokenizer.from_pretrained(modelo_texto)

if device == "cuda":
    modelo_gpt = AutoModelForCausalLM.from_pretrained(
        modelo_texto,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    ).to(device)
else:
    modelo_gpt = AutoModelForCausalLM.from_pretrained(modelo_texto).to(device)

# Modelo base de difusión
modelo_base = "runwayml/stable-diffusion-v1-5"

# Rutas a los modelos personalizados
custom_weights_path = "modelos/realistas/realisticVisionV60B1_v51HyperVAE.safetensors"
lora_path = "modelos/realistas/Noerman_Claire_European_American.safetensors"

# Freesound API Key
freesound_api_key = "your_freesound_api_key_here"
client = freesound.FreesoundClient()
client.set_token(freesound_api_key)

# Cargar modelo de difusión
pipe = StableDiffusionPipeline.from_pretrained(
    modelo_base,
    torch_dtype=torch.float16,
    safety_checker=None,
    variant="fp16"
).to("cuda")

# Cargar pesos personalizados
try:
    print("🔄 Cargando pesos personalizados...")
    state_dict = load_file(custom_weights_path)
    pipe.unet.load_state_dict(state_dict, strict=False)
    print("✅ Pesos cargados desde:", custom_weights_path)
except Exception as e:
    print(f"❌ Error al cargar pesos: {e}")

# Aplica LoRA si existe
if os.path.exists(lora_path):
    pipe.load_lora_weights(lora_path)
    pipe.fuse_lora()

# Directorios de salida
os.makedirs("salida_escenas", exist_ok=True)
os.makedirs("salida_audios", exist_ok=True)

# Lista de escenas
escenas = [
    "Ángelo mira al horizonte mientras la nave se aleja.",
    "Una criatura biomecánica surge de la niebla radioactiva.",
    "Una ciudad futurista iluminada por luces de neón."
]

# === Generación de prompt con GPT-Neo ===
def generar_prompt(texto_escena):
    prompt_base = f"Describe visualmente esta escena: {texto_escena}"
    inputs = tokenizer(prompt_base, return_tensors="pt").to(device)
    output = modelo_gpt.generate(
        **inputs,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    texto_generado = tokenizer.decode(output[0], skip_special_tokens=True)
    return texto_generado.strip()

# === Buscar y descargar audio de Freesound ===
def buscar_audio(escena, output_folder):
    query = f"{escena} sound"
    results = client.text_search(query=query, filter="wav", fields="id,name,previews")

    if results["count"] > 0:
        audio_url = results["results"][0]["previews"]["preview-hq-mp3"]
        audio_filename = f"{output_folder}/{escena.replace(' ', '_')}_audio.mp3"

        with requests.get(audio_url, stream=True) as r:
            if r.status_code == 200:
                with open(audio_filename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
        return audio_filename
    else:
        print(f"❌ No se encontró audio para: {escena}")
        return None

# === Procesamiento principal ===
for i, escena in enumerate(escenas):
    try:
        print(f"\n[{i+1}] Escena: {escena}")

        # Generar prompt con GPT-Neo
        prompt = generar_prompt(escena)
        print(f" → Prompt generado: {prompt}")

        # Generar imagen con Stable Diffusion
        image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]

        output_folder_imagenes = f"salida_escenas/libro_1"
        os.makedirs(output_folder_imagenes, exist_ok=True)

        nombre_imagen = os.path.join(output_folder_imagenes, f"escena_{i+1}.png")
        image.save(nombre_imagen)
        print(f" ✅ Imagen guardada en: {nombre_imagen}")

        output_folder_audios = f"salida_audios/libro_1"
        os.makedirs(output_folder_audios, exist_ok=True)

        audio_file = buscar_audio(escena, output_folder_audios)
        if audio_file:
            print(f" ✅ Audio guardado en: {audio_file}")

    except Exception as e:
        print(f"❌ Error en escena {i+1}: {e}")

print("\n✔️ Proceso completado.")