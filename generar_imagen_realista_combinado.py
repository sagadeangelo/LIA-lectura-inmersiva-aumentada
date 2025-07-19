import os
import sys
import json
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
from transformers import CLIPTokenizer
from compel import Compel
from generador_prompt_inteligente import generar_prompt_ia
from dotenv import load_dotenv

# Cargar el archivo .env para las credenciales de HuggingFace (si las necesitas)
load_dotenv()
hf_token = os.getenv("HF_TOKEN")  # Token de Hugging Face desde .env

# Configuración
libro_id = sys.argv[1] if len(sys.argv) > 1 else "angelo_artefactos"
ruta_libro = Path("libros") / libro_id
config_path = ruta_libro / "config_generacion.json"

# Cargar configuración del libro
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# Cargar rutas y configuraciones
modelo_path = config["ruta_modelo_base"]
negative_prompt = config["negative_prompt"]
lora_activos = config.get("lora", [])

# Configurar el pipeline de Stable Diffusion
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_single_file(
    modelo_path,
    torch_dtype=torch.float32,
    safety_checker=None
).to(device)

# Activar xFormers si está disponible
try:
    pipe.enable_xformers_memory_efficient_attention()
except:
    print("⚠️ Xformers no disponible o no compatible.")

# Preparar Compel para embeddings de prompt
compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)

# Ruta de salida para las imágenes generadas
salida = ruta_libro / "imagenes"
salida.mkdir(parents=True, exist_ok=True)

# Función para generar prompts desde los archivos de escena
def generar_prompts(libro_nombre):
    print(f"📖 Generando prompts para el libro: {libro_nombre}")
    carpeta_escenas = Path(f"libros/{libro_nombre}/escenas")
    
    if not carpeta_escenas.exists():
        print(f"❌ No se encontró la carpeta de escenas: {carpeta_escenas}")
        return

    prompts_path = Path(f"libros/{libro_nombre}/prompts")
    prompts_path.mkdir(parents=True, exist_ok=True)

    for archivo in carpeta_escenas.glob("*.txt"):
        with open(archivo, "r", encoding="utf-8") as f:
            texto_escena = f.read().strip()

        # Generar prompt IA a partir del texto de la escena
        prompt_ia = generar_prompt_ia(texto_escena, estilo="realista", nitidez="alta")

        # Guardar el prompt generado en un archivo de texto
        prompt_file = prompts_path / archivo.name
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt_ia)

        print(f"✅ Prompt generado: {archivo.name}")

# Función para generar imágenes desde los prompts
def generar_imagenes():
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

            # Guardar la imagen generada
            output_path = salida / f"{nombre_escena}.png"
            image.save(output_path)
            print(f"✅ Imagen generada: {output_path.name}")
        except Exception as e:
            print(f"❌ Error al generar imagen para {nombre_escena}: {e}")

if __name__ == "__main__":
    generar_prompts(libro_id)  # Paso 1: Generar prompts para el libro
    generar_imagenes()  # Paso 2: Generar imágenes con esos prompts
