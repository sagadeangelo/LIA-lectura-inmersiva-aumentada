import torch

print("CUDA disponible:", torch.cuda.is_available())
print("Versión de CUDA en PyTorch:", torch.version.cuda)
if torch.cuda.is_available():
    print("Nombre GPU:", torch.cuda.get_device_name(0))
else:
    print("No hay GPU disponible para PyTorch")