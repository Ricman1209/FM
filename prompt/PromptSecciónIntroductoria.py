from ollama import chat
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.LeerDocumento import leer_manual
import json, re

texto_manual = leer_manual()

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
                "Evita explicaciones largas o ejemplos innecesarios. No escribas texto fuera del JSON. "
                "Formato requerido:\n"
                "{\n"
                "  \"propósito\": \"Describe brevemente el objetivo general del documento.\",\n"
                "  \"ámbito\": \"Delimita el contenido y el alcance del manual.\",\n"
                "  \"audiencia\": \"Indica a quién va dirigido el documento.\",\n"
                "  \"objetivo\": \"Explica qué busca lograr el manual.\",\n"
                "  \"alcance\": \"Detalla brevemente a qué sistemas o procesos aplica.\",\n"
                "  \"área\": \"Menciona el área o departamento responsable.\"\n"
                "}"
            )
        },
        {
            "role": "user",
            "content": (
                "Genera la sección introductoria del manual con base en el siguiente contenido técnico. "
                "Redacta cada campo con estilo institucional y técnico, procurando que toda la sección quepa en una sola página:\n\n"
                f"{texto_manual}"
            )
        }
    ]
)


#parche ia ------------------------------------------------------------------------------
# Parche robusto para procesar JSON devuelto por el modelo
raw = response.message.content.strip()

match = re.search(r"(\[.*\]|\{.*\})", raw, re.DOTALL)
if match:

    json_text = match.group(0)
    # Limpieza de formato
    json_text = json_text.replace("\\", "\\\\")
    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    json_text = re.sub(r'\n+', ' ', json_text)     
    json_text = re.sub(r'"\s+"', ' ', json_text)    
    json_text = re.sub(r'\s{2,}', ' ', json_text)    

    try:
        Glosario = json.loads(json_text)
        # Asegurar que sea lista
        if isinstance(Glosario, dict):
            Glosario = [Glosario]
    except json.JSONDecodeError as e:
        print(f"⚠️ Error al decodificar JSON ({e}), usando texto plano.")
        Glosario = [{"termino": "Error", "significado": raw}]
else:
    print("⚠️ No se encontró JSON válido, usando texto plano.")
    Glosario = [{"termino": "Error", "significado": raw}]



for item in Glosario:
    if "signado" in item:
        item["significado"] = item.pop("signado")

# Validación final
if not Glosario or not isinstance(Glosario, list):
    Glosario = [{"termino": "Error", "significado": "El modelo no generó contenido válido."}]

if isinstance(Glosario, list) and len(Glosario) > 0:
    data = Glosario[0]  # Tomar el primer diccionario dentro de la lista
elif isinstance(Glosario, dict):
    data = Glosario
else:
    data = {}

Propósito = data.get("propósito", "").strip()
Ámbito = data.get("ámbito", "").strip()
Audiencia = data.get("audiencia", "").strip()
Objetivo = data.get("objetivo", "").strip()
Alcance = data.get("alcance", "").strip()
Área = data.get("área", "").strip()
#parche ia ------------------------------------------------------------------------------
