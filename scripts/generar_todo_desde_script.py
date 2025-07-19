import os
import subprocess
from pathlib import Path
import argparse
import sys
import shutil

# 📦 Clonar el repositorio si no existe
if os.path.exists("LIA-lectura-inmersiva-aumentada"):
    shutil.rmtree("LIA-lectura-inmersiva-aumentada")
subprocess.run(["git", "clone", "https://github.com/sagadeangelo/LIA-lectura-inmersiva-aumentada.git"], check=True)
os.chdir("LIA-lectura-inmersiva-aumentada")

# 🧪 Instalar dependencias
subprocess.run(["pip", "install", "diffusers", "transformers", "accelerate", "safetensors", "peft", "compel", "python-dotenv"])

# 🔐 Crear archivo .env
env_content = '''
FREESOUND_API_KEY=tu_clave_de_freesound_aqui
HUGGINGFACE_TOKEN=tu_token_de_huggingface_aqui
'''.strip()
Path(".env").write_text(env_content)
print("✅ .env creado")

# ✅ Ejecutar script principal con argumentos
args = argparse.Namespace(
    libro="libros/angelo_ditox/angelo_ditox.txt",
    ruta="libros/angelo_ditox"
)

sys.argv = ["scripts/generar_todo_desde_libro.py"] + [f"--{k}={v}" for k, v in vars(args).items()]
with open("scripts/generar_todo_desde_libro.py", encoding="utf-8") as f:
    exec(f.read())