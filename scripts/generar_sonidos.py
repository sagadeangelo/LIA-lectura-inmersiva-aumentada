import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from keybert import KeyBERT

# Cargar variables de entorno
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise ValueError("❌ ACCESS_TOKEN no encontrado en .env")

# Inicializar modelo de extracción
kw_model = KeyBERT()

# Palabras clave permitidas (sonoras y universales)
VOCABULARIO_SONIDO = {
    "fire", "rain", "forest", "storm", "wind", "explosion", "battle",
    "whispers", "heartbeat", "scream", "footsteps", "ocean", "water",
    "magic", "laugh", "cry", "door", "metal", "attack", "danger",
    "alarm", "echo", "machine", "drone", "gun", "thunder", "roar",
    "growl", "clap", "whistle", "bell", "engine", "clock", "glass",
    "birds", "wolves", "sword", "river", "running", "crowd", "howl",
    "mechanism", "boom", "smoke", "flame", "energy", "portal", "mystery",
    "darkness", "light", "electric", "laser", "action", "battlefield",
    "screech", "swordfight", "tension", "fear", "joy", "calm"
}

# Función para extraer palabras clave relevantes
def extraer_palabras_clave(texto):
    keywords = kw_model.extract_keywords(texto, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
    palabras_utiles = [kw for kw, score in keywords if kw.lower() in VOCABULARIO_SONIDO]
    return list(dict.fromkeys(palabras_utiles))[:3]  # máximo 3

# Función para descargar sonido
def descargar_sonido(sound_url, carpeta_destino, nombre_archivo):
    response = requests.get(sound_url)
    if response.status_code == 200:
        with open(os.path.join(carpeta_destino, nombre_archivo), 'wb') as f:
            f.write(response.content)
        print(f"✅ Sonido guardado: {nombre_archivo}")
    else:
        print(f"❌ Error al descargar el sonido: {response.status_code}")

# Buscar y descargar sonidos desde freesound
def buscar_y_descargar_sonidos(query, carpeta_destino, archivo_log, escena_nombre):
    if not query.strip():
        print("⚠️  Escena sin palabras clave válidas para sonido, se omite descarga.")
        archivo_log.write(f"{escena_nombre} => SIN PALABRAS CLAVE\n")
        return

    url = 'https://freesound.org/apiv2/search/text/'
    headers = { 'Authorization': f'Bearer {ACCESS_TOKEN}' }
    params = { 'query': query }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        for sound in data['results']:
            if 'previews' in sound and 'preview-hq-mp3' in sound['previews']:
                sound_url = sound['previews']['preview-hq-mp3']
                nombre_archivo = f"{sound['id']}.mp3"
                descargar_sonido(sound_url, carpeta_destino, nombre_archivo)
                archivo_log.write(f"{escena_nombre} => OK: {nombre_archivo} ({query})\n")
                return
        print(f"🔇 No se encontraron sonidos para '{query}'")
        archivo_log.write(f"{escena_nombre} => SIN RESULTADOS ({query})\n")
    else:
        print(f"❌ Error API: {response.status_code}")
        archivo_log.write(f"{escena_nombre} => ERROR API ({response.status_code})\n")

# Recorrer escenas del libro
def generar_sonidos(libro_nombre):
    print(f"📖 Iniciando generación de sonidos para el libro: {libro_nombre}")
    carpeta_escenas = Path(f"libros/{libro_nombre}/escenas")
    log_path = Path("log_sonidos.txt")

    if not carpeta_escenas.exists():
        print(f"❌ No se encontró la carpeta: {carpeta_escenas}")
        return

    with open(log_path, "w", encoding="utf-8") as archivo_log:
        for archivo in carpeta_escenas.rglob("*.txt"):
            print(f"\n📄 Procesando archivo: {archivo.name}")
            with open(archivo, "r", encoding="utf-8") as f:
                escena = f.read().strip()

            capitulo_actual = archivo.stem.split("_")[1]
            ruta_capitulo = Path(f"libros/{libro_nombre}/audios/cap_{capitulo_actual}")
            os.makedirs(ruta_capitulo, exist_ok=True)

            palabras_clave = extraer_palabras_clave(escena)
            if palabras_clave:
                query = ' '.join(palabras_clave)
                print(f"🔎 Palabras clave para búsqueda: {palabras_clave}")
                buscar_y_descargar_sonidos(query, ruta_capitulo, archivo_log, archivo.name)
            else:
                print(f"⚠️  Escena sin palabras clave válidas para sonido, se omite descarga.")
                archivo_log.write(f"{archivo.name} => SIN PALABRAS CLAVE\n")

    print(f"\n📝 Log final guardado en: {log_path.resolve()}")

# Ejecutar desde consola
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        generar_sonidos(sys.argv[1])
    else:
        print("❌ Debes indicar el nombre del libro. Ejemplo: python generar_sonidos.py angelo_artefactos")