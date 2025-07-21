import os

# Ruta base donde están los libros
base_dir = "libros"

# Carpetas en las que se necesita agregar .gitkeep
carpetas_objetivo = ["imagenes", "audios"]

# Recorremos cada libro
for libro in os.listdir(base_dir):
    ruta_libro = os.path.join(base_dir, libro)
    if os.path.isdir(ruta_libro):
        for carpeta in carpetas_objetivo:
            ruta_carpeta = os.path.join(ruta_libro, carpeta)
            if os.path.isdir(ruta_carpeta):
                ruta_gitkeep = os.path.join(ruta_carpeta, ".gitkeep")
                # Crear el archivo vacío si no existe
                if not os.path.exists(ruta_gitkeep):
                    with open(ruta_gitkeep, "w", encoding="utf-8") as f:
                        f.write("")  # Archivo vacío
                    print(f"✅ .gitkeep creado en: {ruta_gitkeep}")
                else:
                    print(f"ℹ️ Ya existía: {ruta_gitkeep}")
