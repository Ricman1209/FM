from ollama import chat
from utils.LeerDocumento import leer_manual
import json, re


texto_manual = leer_manual()


response = chat(
    model="llama2:7b",
    messages=[
        {
            "role": "system",
                "content": (
                    "Eres un asistente que genera glosarios técnicos a partir del contenido de un manual. "
                    "Responde ÚNICAMENTE con un JSON válido y NADA más. "
                    "No escribas texto antes ni después del JSON. "
                    "Ejemplo de formato:\n"
                    "[{\"termino\": \"DNS\", \"significado\": \"Sistema de nombres de dominio.\"}, "
                    "{\"termino\": \"IP\", \"significado\": \"Protocolo de Internet.\"}]"
            )
        },
        {
            "role": "user",
            "content": f"Genera un glosario para el siguiente manual:\n\n{texto_manual}"
        }
    ]
)


#Parche dado por IA--------------------------------------------------------
raw = response.message.content

# Buscar JSON en la respuesta
match = re.search(r"\[.*\]", raw, re.DOTALL)
if match:
    json_text = match.group(0)
    # Limpieza: arreglar barras invertidas y comas colgantes
    json_text = json_text.replace("\\", "\\\\")              # Escapar correctamente las barras
    json_text = re.sub(r",\s*}", "}", json_text)             # Eliminar comas antes de }
    json_text = re.sub(r",\s*]", "]", json_text)             # Eliminar comas antes de ]
    try:
        Glosario = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"⚠️ Error al decodificar JSON ({e}), usando texto plano.")
        Glosario = [{"termino": "Error", "significado": raw.strip()}]
else:
    print("⚠️ No se encontró JSON válido, usando texto plano.")
    Glosario = [{"termino": "Error", "significado": raw.strip()}]


for item in Glosario:
    if "signado" in item:
        item["significado"] = item.pop("signado")



