import os
import shutil
import subprocess
from pathlib import Path
import argparse

# 1. Clonar el repositorio (solo si no está)
if os.path.exists("LIA-lectura-inmersiva-aumentada"):
    shutil.rmtree("LIA-lectura-inmersiva-aumentada")

# Usa subprocess para ejecutar git clone (válido en scripts Python)
subprocess.run(["git", "clone", "https://github.com/sagadeangelo/LIA-lectura-inmersiva-aumentada.git"])

# Cambiar directorio usando os
os.chdir("LIA-lectura-inmersiva-aumentada")

# 2. Instalar dependencias necesarias con subprocess
subprocess.run([
    "pip", "install", "diffusers", "transformers", "accelerate", 
    "safetensors", "peft", "compel", "python-dotenv"
])

# 3. Crear archivo .env con API keys (modifica los valores)
env_content = """
FREESOUND_API_KEY=tu_clave_de_freesound_aqui
HUGGINGFACE_TOKEN=tu_token_de_huggingface_aqui
""".strip()
Path(".env").write_text(env_content)
print("✅ .env creado")

# 4. Procesar argumentos (de ejemplo, puedes modificar)
parser = argparse.ArgumentParser()
parser.add_argument("--libro", required=True, help="Ruta al archivo .txt del libro")
parser.add_argument("--ruta", required=True, help="Carpeta del libro")
args = parser.parse_args()

# Aquí pondrías la lógica principal de tu script
print(f"Procesando libro en: {args.libro}")
print(f"Ruta para guardar resultados: {args.ruta}")

# [Inserta aquí el resto de código que procesará el libro]