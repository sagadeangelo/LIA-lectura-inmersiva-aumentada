import torch

# Verificar si la GPU está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando: {device}")
