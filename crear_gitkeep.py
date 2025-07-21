import os

# Ruta base donde están los libros
base_dir = "libros"

# Todas las subcarpetas necesarias para cada libro
carpetas_objetivo = ["imagenes", "audios", "escenas", "prompts"]

# Recorremos cada carpeta de libro
for libro in os.listdir(base_dir):
    ruta_libro = os.path.join(base_dir, libro)
    if os.path.isdir(ruta_libro):
        for carpeta in carpetas_objetivo:
            ruta_carpeta = os.path.join(ruta_libro, carpeta)
            # Crear la carpeta si no existe
            os.makedirs(ruta_carpeta, exist_ok=True)
            # Crear archivo .gitkeep vacío
            ruta_gitkeep = os.path.join(ruta_carpeta, ".gitkeep")
            if not os.path.exists(ruta_gitkeep):
                with open(ruta_gitkeep, "w", encoding="utf-8") as f:
                    f.write("")
                print(f"✅ .gitkeep creado en: {ruta_gitkeep}")
            else:
                print(f"ℹ️ Ya existía: {ruta_gitkeep}")
