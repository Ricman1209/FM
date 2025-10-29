from ollama import chat
from utils.LeerDocumento import leer_manual
import json
import re

texto_manual = leer_manual()

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

# Convertir respuesta a JSON
try:
    datos_diagrama = json.loads(response.message.content)
except Exception:
    datos_diagrama = {"titulo": "Proceso", "pasos": []}

titulo_diagrama = datos_diagrama['titulo']
pasos_diagrama = datos_diagrama['pasos']

# 🧹 Limpieza de pasos antes de pasarlos al generador
def limpiar_texto(paso):
    """
    Si Ollama devuelve objetos o texto con llaves y etiquetas ('etiqueta', 'acción', etc.),
    los limpia para dejar solo el texto legible del procedimiento.
    """
    if isinstance(paso, dict):
        # Si Ollama devolvió un diccionario, concatenamos sus valores
        return " - ".join(str(v) for v in paso.values())
    elif isinstance(paso, str):
        # Si devolvió un string con formato de diccionario, limpiamos con regex
        limpio = re.sub(r"['{}]", "", paso)
        limpio = limpio.replace("etiqueta:", "").replace("acción:", "")
        limpio = re.sub(r"\s+", " ", limpio).strip()
        return limpio
    return str(paso)

# Aplicar limpieza a todos los pasos
pasos_diagrama = [limpiar_texto(p) for p in pasos_diagrama]

#print(f"📘 Título: {titulo_diagrama}")
#print(f"🧩 Pasos limpios ({len(pasos_diagrama)}):")
#for p in pasos_diagrama:
#    print(f"  - {p}")
