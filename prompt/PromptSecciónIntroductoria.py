from ollama import chat
from services.readerService import leer_manual
import json, re

def generar_seccion_introductoria():
    """
    Genera dinámicamente la sección introductoria con ayuda de la IA.
    Retorna un diccionario con los campos generados.
    """
    try:
        texto_manual = leer_manual()
    except FileNotFoundError:
        print("⚠️ No se encontró templates/Manual.docx. Sube primero un archivo.")
        return {}

    response = chat(
        model="llama2:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente especializado en redacción de manuales técnicos. "
                    "Debes generar una sección introductoria formal y clara, adecuada para ocupar solo una página. "
                    "Responde SIEMPRE en español y SOLO en formato JSON válido. "
                    "Cada campo debe tener entre una y dos oraciones, con redacción técnica, precisa y sin redundancias. "
                    "Evita ejemplos o texto fuera del JSON."
                )
            },
            {
                "role": "user",
                "content": (
                    "Genera la sección introductoria del manual con base en el siguiente contenido técnico:\n\n"
                    f"{texto_manual}"
                )
            }
        ]
    )

    raw = response.message.content.strip()
    match = re.search(r"(\{.*\})", raw, re.DOTALL)
    data = {}

    if match:
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            print("⚠️ Error al decodificar JSON, usando texto plano.")
    else:
        print("⚠️ No se encontró JSON válido.")

    return {
        "propósito": data.get("propósito", ""),
        "ámbito": data.get("ámbito", ""),
        "audiencia": data.get("audiencia", ""),
        "objetivo": data.get("objetivo", ""),
        "alcance": data.get("alcance", ""),
        "área": data.get("área", "")
    }
