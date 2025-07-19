import torch

# Verifica si CUDA está disponible
if torch.cuda.is_available():
    print(f"Usando GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA no está disponible. Usando CPU.")




