# LIA – Lectura Inmersiva Aumentada

Proyecto educativo que transforma libros en experiencias inmersivas mediante inteligencia artificial. Utiliza Flutter para la interfaz, Python para la generación de contenido visual y sonoro, y Stable Diffusion local para crear escenas ilustradas a partir del texto.

---

## 🚀 Características principales

- Lectura inmersiva sincronizada con imágenes generadas por IA.
- Sonidos ambientales automáticos basados en el contenido del texto.
- Soporte para múltiples libros, capítulos y escenas.
- Arquitectura local sin dependencia de servicios externos.
- Integración con modelos personalizados (`.safetensors`, `.ckpt`, etc.)

---

## 📁 Estructura del proyecto

```
LIA-lectura-inmersiva-aumentada/
├── libros/              # Archivos .json con libros y escenas
│   └── [LIBRO]/         # Carpeta por cada libro
│       ├── escenas/     # Archivos de texto por escena
│       ├── imagenes/    # Imágenes generadas por IA
│       ├── sonidos/     # Audios ambientales descargados
│       └── prompts/     # Prompts generados automáticamente
├── modelos/             # Modelos IA locales (no incluidos)
├── lib/                 # Código Flutter principal
├── scripts/             # Scripts Python de generación
├── venv/                # Entorno virtual local (ignorado)
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Tecnologías utilizadas

- **Flutter** – interfaz móvil y de escritorio.
- **Python 3.11** – backend y automatización.
- **Stable Diffusion local** – generación de imágenes por escena.
- **Compel** – prompts IA con mayor precisión.
- **Pixabay API** – sonidos ambientales libres.
- **FFmpeg** – conversión y edición de audio.
- **Git/GitHub** – control de versiones.

---

## 💾 Instalación local (modo desarrollador)

```bash
git clone https://github.com/sagadeangelo/LIA-lectura-inmersiva-aumentada.git
cd LIA-lectura-inmersiva-aumentada

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # En Linux/Mac: source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script de generación de imágenes
python scripts/generar_imagenes_desde_cache.py
```

---

## ⚠️ Modelos IA (no incluidos en el repositorio)

Este repositorio no contiene los modelos IA por su gran tamaño.

Por favor, coloca tus modelos en la siguiente carpeta:

```
/modelos/
```

Archivos compatibles:
- `.safetensors`
- `.ckpt`
- `.pth`

Estos archivos deben ser configurados en tu archivo de parámetros JSON correspondiente.

---

## 🧠 Créditos

Proyecto desarrollado por [Miguel Tovar Amral](https://github.com/sagadeangelo) como parte del sistema educativo **LIA OS**.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
