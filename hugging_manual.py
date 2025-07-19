from huggingface_hub import snapshot_download

print("Descargando modelo completo...")
snapshot_download("EleutherAI/gpt-neo-1.3B", force_download=True)
print("Descarga completada.")