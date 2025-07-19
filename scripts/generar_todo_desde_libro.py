
# 📦 1. Clonar el repositorio (solo si no está)
!rm -rf LIA-lectura-inmersiva-aumentada
!git clone https://github.com/sagadeangelo/LIA-lectura-inmersiva-aumentada.git
%cd LIA-lectura-inmersiva-aumentada
# 🧪 2. Instalar dependencias necesarias
!pip install diffusers transformers accelerate safetensors peft compel python-dotenv
# 🔐 3. Crear archivo .env con tu API KEY de Freesound y HuggingFace
# 🔁 Reemplaza con tus claves reales antes de ejecutar
from pathlib import Path

env_content = """
FREESOUND_API_KEY=tu_clave_de_freesound_aqui
HUGGINGFACE_TOKEN=tu_token_de_huggingface_aqui
""".strip()

Path(".env").write_text(env_content)
print("✅ .env creado")
# ✅ 4. Ejecutar el script principal con argumentos simulados
import argparse
import sys

# 📘 Cambia si usas otro libro o ruta
args = argparse.Namespace(
    libro="libros/angelo_ditox/angelo_ditox.txt",  # RUTA AL .TXT
    ruta="libros/angelo_ditox"                     # Carpeta del libro
)

sys.argv = ["scripts/generar_todo_desde_libro.py"] + [f"--{k}={v}" for k, v in vars(args).items()]
exec(open("scripts/generar_todo_desde_libro.py").read())
