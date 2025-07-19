from transformers import AutoTokenizer, AutoModelForCausalLM

# Nombre del modelo con soporte para .safetensors
model_name = "EleutherAI/gpt-neo-1.3B"

# Descarga y cachea el tokenizer y el modelo
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)