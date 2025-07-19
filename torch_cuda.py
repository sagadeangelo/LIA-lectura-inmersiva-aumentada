import torch

# Verificar memoria antes de la ejecución
print(f"Memoria utilizada antes: {torch.cuda.memory_allocated() / 1024**2} MB")
print(f"Memoria reservada antes: {torch.cuda.memory_reserved() / 1024**2} MB")

# Ejecutar tu código de generación de imágenes o tareas de PyTorch

# Liberar la memoria de la GPU después de la operación
torch.cuda.empty_cache()

# Verificar memoria después de la ejecución
print(f"Memoria utilizada después: {torch.cuda.memory_allocated() / 1024**2} MB")
print(f"Memoria reservada después: {torch.cuda.memory_reserved() / 1024**2} MB")

# Si ves que la memoria no se libera adecuadamente, puedes intentar configurar `torch.no_grad()`
