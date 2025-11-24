from ollama import chat
from services.readerService import leer_manual
import json
import re

def generar_datos_diagrama():
    """
    Genera los datos del diagrama (título y pasos) analizando el contenido del Manual.docx con Ollama.
    Retorna un diccionario con:
    {
        "titulo_diagrama": str,
        "pasos_diagrama": list[str]
    }
    """
    try:
        texto_manual = leer_manual()
    except FileNotFoundError:
        print("⚠️ No se encontró templates/Manual.docx. Sube primero un archivo.")
        return {"titulo_diagrama": "Proceso general", "pasos_diagrama": []}

    response = chat(
        model="llama2:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en análisis de procedimientos técnicos. "
                    "Tu tarea es identificar los pasos secuenciales de un proceso "
                    "y devolverlos estrictamente en formato JSON válido. "
                    "No incluyas texto adicional ni explicaciones."
                    "\nFormato esperado:\n"
                    "{ \"titulo\": \"nombre_del_proceso\", \"pasos\": [\"Paso 1...\", \"Paso 2...\", ...] }"
                )
            },
            {
                "role": "user",
                "content": f"Analiza el siguiente manual y genera los pasos del diagrama de flujo:\n\n{texto_manual}"
            }
        ]
    )

    # Intentar decodificar JSON de respuesta
    try:
        raw = response.message.content
        # Buscar bloque JSON entre llaves
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            json_text = match.group(0)
            datos_diagrama = json.loads(json_text)
        else:
            # Fallback si no encuentra llaves, intentar parsear todo (aunque probablemente falle)
            datos_diagrama = json.loads(raw)
    except Exception as e:
        print(f"⚠️ No se pudo decodificar el JSON ({e}), usando valores por defecto.")
        datos_diagrama = {"titulo": "Proceso", "pasos": []}

    titulo_diagrama = datos_diagrama.get("titulo", "Proceso sin título")
    pasos_diagrama = datos_diagrama.get("pasos", [])

    # Limpieza de texto
    def limpiar_texto(paso):
        if isinstance(paso, dict):
            return " - ".join(str(v) for v in paso.values())
        elif isinstance(paso, str):
            limpio = re.sub(r"['{}]", "", paso)
            limpio = limpio.replace("etiqueta:", "").replace("acción:", "")
            limpio = re.sub(r"\s+", " ", limpio).strip()
            return limpio
        return str(paso)

    pasos_diagrama = [limpiar_texto(p) for p in pasos_diagrama]

    return {
        "titulo_diagrama": titulo_diagrama,
        "pasos_diagrama": pasos_diagrama
    }
