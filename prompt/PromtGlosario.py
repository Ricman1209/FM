from ollama import chat
from services.readerService import leer_manual
import json, re
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
                    "Asegúrate de devolver UNA SOLA lista de objetos, no múltiples listas separadas. "
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
    # 1. Encontrar el bloque desde el primer '[' hasta el último ']'
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        print("⚠️ No se encontró JSON válido, usando entrada plana.")
        return [{"termino": "Error", "significado": raw.strip()}]

    json_text = match.group(0)
    
    # 2. Unificar listas fragmentadas: Reemplazar "] ... [" por ","
    # Esto maneja casos donde el LLM devuelve múltiples listas separadas por texto
    json_text = re.sub(r"\][^\[]*\[", ",", json_text)

    json_text = json_text.replace("\\", "\\\\")
    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    print(f"🔍 RAW JSON GLOSARIO: {json_text}")

    try:
        data = json.loads(json_text)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError as e:
        print(f"⚠️ Error al decodificar JSON ({e}), usando texto plano.")
        data = [{"termino": "Error", "significado": raw.strip()}]

    # Normalizar posibles claves mal devueltas
    normalized_data = []
    for item in data:
        print(f"🔍 ITEM KEYS: {item.keys()}")
        new_item = {}
        # Buscar termino
        if "termino" in item:
            new_item["termino"] = item["termino"]
        elif "Termino" in item:
            new_item["termino"] = item["Termino"]
        elif "term" in item:
            new_item["termino"] = item["term"]
        else:
            new_item["termino"] = "Desconocido"

        # Buscar significado
        if "significado" in item:
            new_item["significado"] = item["significado"]
        elif "Significado" in item:
            new_item["significado"] = item["Significado"]
        elif "definition" in item:
            new_item["significado"] = item["definition"]
        elif "signado" in item:
            new_item["significado"] = item["signado"]
        else:
            new_item["significado"] = "" # Dejar vacío para filtrar después
            
        # Validar y limpiar
        term = str(new_item.get("termino", "")).strip()
        meaning = str(new_item.get("significado", "")).strip()
        
        print(f"🔍 DEBUG ITEM: Term='{term}' | Meaning='{meaning}'")

        # Solo agregar si ambos campos tienen contenido y no son los valores por defecto de error
        if len(term) > 0 and len(meaning) > 0 and term != "Desconocido" and meaning != "Sin definición":
            print(f"   ✅ ACEPTADO: {term}")
            normalized_data.append({"termino": term, "significado": meaning})
        else:
            print(f"   ❌ RECHAZADO: {term}")
    
    data = normalized_data

    # Validación final
    if not isinstance(data, list) or not data:
        data = [{"termino": "Error", "significado": "El modelo no generó contenido válido."}]

    return data
