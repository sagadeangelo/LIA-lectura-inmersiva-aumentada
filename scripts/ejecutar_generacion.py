import os
import argparse
from dotenv import load_dotenv
from scripts.generar_todo_desde_libro import main

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar argumentos simulados
parser = argparse.ArgumentParser()
parser.add_argument("--libro", required=True, help="Ruta al archivo .txt del libro")
parser.add_argument("--ruta", required=True, help="Ruta a la carpeta del libro")
args = parser.parse_args()

# Ejecutar función principal
main(args.libro, args.ruta)
