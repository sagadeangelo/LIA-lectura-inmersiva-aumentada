def generar_prompt_ia(texto_escena, estilo="infantil", nitidez="media"):
    estilo = estilo.lower()
    nitidez = nitidez.lower()

    base = texto_escena.strip().capitalize()

    # Estilo visual
    if estilo == "infantil":
        estilo_descriptivo = (
            "storybook illustration, pastel colors, magical lighting, soft outlines"
        )
    elif estilo == "realista":
        estilo_descriptivo = (
            "highly detailed, cinematic, realistic style, natural lighting"
        )
    else:
        estilo_descriptivo = "fantasy concept art, digital painting"

    # Nivel de nitidez
    if nitidez == "alta":
        detalle = "sharp focus, 4k details, ultra-detailed, clean edges"
    elif nitidez == "media":
        detalle = "soft shading, moderately detailed, fantasy mood"
    else:
        detalle = "soft blur, dreamlike, low contrast"

    prompt_final = f"{base}, {estilo_descriptivo}, {detalle}"
    return prompt_final
