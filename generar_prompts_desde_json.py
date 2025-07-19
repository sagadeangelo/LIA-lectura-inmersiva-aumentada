import os
import sys
from pathlib import Path
from generador_prompt_inteligente import generar_prompt_ia

# ⚙️ Nombre del libro recibido por argumento
nombre_libro = sys.argv[1] if len(sys.argv) > 1 else "libro_demo"

# 📂 Ruta base
base_path = Path("libros") / nombre_libro
escenas_path = base_path / "escenas"
prompts_path = base_path / "prompts"

# 📁 Crear carpeta de prompts si no existe
prompts_path.mkdir(parents=True, exist_ok=True)

# 🔁 Recorremos todos los archivos .txt dentro de escenas/
for archivo in escenas_path.glob("*.txt"):
    with open(archivo, "r", encoding="utf-8") as f:
        texto_escena = f.read().strip()

    # 🧠 Generar prompt IA a partir del texto
    prompt_ia = generar_prompt_ia(texto_escena, estilo="realista", nitidez="alta")

    # 💾 Guardar prompt con el mismo nombre que el archivo de escena
    prompt_file = prompts_path / archivo.name
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt_ia)

    print(f"✅ Prompt generado: {prompt_file.name}")

print("✨ Todos los prompts fueron generados correctamente.")
