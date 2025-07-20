import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

CONFIG_DIR   = "modelos/config"
PROMPTS_DIR  = "prompts"
OUTPUT_DIR   = "imagenes_generadas"
META_DIR     = "imagenes_generadas/metadata"   # opcional

# 👉 Cambia esto si invocas tu webui con otro comando
#    Por ejemplo, en Windows podrías usar ["python", "webui.py"]
cmd_base = ["python", "launch.py", "--skip-torch-cuda-test"]

# ------------------------------------------------------------------------
def build_command(config_json, prompt_text, out_png):
    """Devuelve la lista de argumentos para subprocess.run()."""
    cmd = cmd_base + [
        "--prompt", prompt_text.replace('"', '\\"'),
        "--negative_prompt", config_json.get("negative_prompt", "").replace('"', '\\"'),
        "--ckpt", config_json["ruta_modelo_base"],
        "--outdir", str(Path(out_png).parent),
        "--steps", "25",
        "--fname", Path(out_png).stem  # fuerza nombre de archivo
    ]

    # Añadir cada LoRA
    for l in config_json.get("lora", []):
        cmd += ["--lora", f'{l["ruta"]}:{l.get("peso",1.0)}']

    return cmd

# ------------------------------------------------------------------------
def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(META_DIR).mkdir(parents=True, exist_ok=True)

    json_files = [p for p in Path(CONFIG_DIR).glob("*.json")]

    if not json_files:
        print("❌ No se encontraron archivos .json en", CONFIG_DIR)
        return

    for cfg_path in json_files:
        base_name   = cfg_path.stem   # bosque_magico.json → bosque_magico
        prompt_file = Path(PROMPTS_DIR, base_name + ".txt")
        out_png     = Path(OUTPUT_DIR, base_name + ".png")
        meta_file   = Path(META_DIR,  base_name + ".meta.json")

        if not prompt_file.exists():
            print(f"⚠️  Prompt no encontrado: {prompt_file}")
            continue

        # Leer archivos
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()

        print(f"🖼️  Generando: {base_name}.png")
        cmd = build_command(cfg, prompt_text, out_png)
        print("   ➜", " ".join(cmd))

        try:
            subprocess.run(cmd, check=True)
            print("   ✅ Imagen creada:", out_png)
        except subprocess.CalledProcessError as e:
            print("   ❌ Error al generar la imagen:", e)
            continue

        # Guardar metadatos útiles
        meta = {
            "datetime": datetime.now().isoformat(timespec="seconds"),
            "prompt": prompt_text,
            "negative_prompt": cfg.get("negative_prompt", ""),
            "modelo_base": cfg["ruta_modelo_base"],
            "loras": cfg.get("lora", [])
        }
        meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

# ------------------------------------------------------------------------
if __name__ == "__main__":
    main()