import argparse
import os

def procesar_libro(libro_path, ruta_destino):
    print(f"📖 Procesando libro en: {libro_path}")
    print(f"📁 Carpeta de destino: {ruta_destino}")
    
    # Aquí va la lógica real que transforma el texto, genera audio, imágenes, etc.
    # Por ahora dejamos un mensaje de prueba:
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
        print("✅ Carpeta creada")

    with open(libro_path, "r", encoding="utf-8") as f:
        contenido = f.read()
        print(f"📝 El libro tiene {len(contenido.split())} palabras")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--libro", required=True, help="Ruta al archivo .txt del libro")
    parser.add_argument("--ruta", required=True, help="Carpeta destino para guardar resultados")
    args = parser.parse_args()

    procesar_libro(args.libro, args.ruta)