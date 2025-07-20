import freesound

# Sustituye con tu token real de Freesound.org
API_KEY = "Fpwm7P0sllNW3dztbbZcVQXFbEztmy"

client = freesound.FreesoundClient()
client.set_token(API_KEY, "token")

query = input("🔎 ¿Qué sonido quieres buscar?: ")
results = client.text_search(query=query, fields="id,name,previews", page_size=5)

for sound in results:
    print(f"\n🔊 Nombre: {sound.name}")
    print(f"▶️ Preview: {sound.previews.preview_lq_mp3}")
    print("—" * 40)