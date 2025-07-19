import os
import shutil

# 📂 Ruta base (ajusta si lo colocas en otro directorio)
RAIZ = os.path.dirname(__file__)
CARPETA_LEGACY = os.path.join(RAIZ, "archivos_legacy")
os.makedirs(CARPETA_LEGACY, exist_ok=True)

# 📦 Lista de archivos obsoletos que deseas mover
archivos_a_mover = [
    "generar_imagen_realista_combinado.py",
    "generar_imagenes_desde_cache.py",
    "generar_imagen_ia.py",
    "generar_sd_desde_prompt.py",
    "generar_prompts_desde_json.py"
]

# 🔁 Mover archivos si existen
archivos_movidos = []

for nombre in archivos_a_mover:
    origen = os.path.join(RAIZ, nombre)
    destino = os.path.join(CARPETA_LEGACY, nombre)

    if os.path.exists(origen):
        shutil.move(origen, destino)
        archivos_movidos.append(nombre)
        print(f"✅ Movido a legacy: {nombre}")
    else:
        print(f"⚠️ No encontrado: {nombre}")

# 🧾 Resumen
if archivos_movidos:
    print("\n🗂️ Archivos movidos correctamente:")
    for archivo in archivos_movidos:
        print(f" - {archivo}")
else:
    print("\n📭 No se movió ningún archivo.")
