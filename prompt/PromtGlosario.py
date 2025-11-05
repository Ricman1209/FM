from ollama import chat
from services.readerService import leer_manual
import json, re

def generar_glosario():
    """
    Lee Manual.docx y genera un glosario con la IA.
    Devuelve: list[{"termino": str, "significado": str}]
    """
    try:
        texto_manual = leer_manual()
    except FileNotFoundError:
        print("⚠️ No se encontró templates/Manual.docx. Sube primero un archivo.")
        return []

    response = chat(
        model="llama2:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente que genera glosarios técnicos a partir del contenido de un manual. "
                    "Responde ÚNICAMENTE con un JSON válido y NADA más. "
                    "Formato: "
                    "[{\"termino\": \"DNS\", \"significado\": \"Sistema de nombres de dominio.\"}, "
                    "{\"termino\": \"IP\", \"significado\": \"Protocolo de Internet.\"}]"
                ),
            },
            {
                "role": "user",
                "content": f"Genera un glosario para el siguiente manual:\n\n{texto_manual}",
            },
        ],
    )

    raw = response.message.content

    # Extraer JSON (lista) y sanear
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        print("⚠️ No se encontró JSON válido, usando entrada plana.")
        return [{"termino": "Error", "significado": raw.strip()}]

    json_text = match.group(0)
    json_text = json_text.replace("\\", "\\\\")
    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    try:
        data = json.loads(json_text)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError as e:
        print(f"⚠️ Error al decodificar JSON ({e}), usando texto plano.")
        data = [{"termino": "Error", "significado": raw.strip()}]

    # Normalizar posibles claves mal devueltas
    for item in data:
        if "signado" in item:
            item["significado"] = item.pop("signado")

    # Validación final
    if not isinstance(data, list) or not data:
        data = [{"termino": "Error", "significado": "El modelo no generó contenido válido."}]

    return data
