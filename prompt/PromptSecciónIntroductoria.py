from ollama import chat
from services.readerService import leer_manual
import json, re
import json, re

def parse_fallback(text):
    """
    Intenta extraer los campos usando expresiones regulares si el JSON falla.
    Soporta formato texto plano (Propósito: ...) y JSON mal formado ("propósito": "...").
    """
    fields = ["propósito", "ámbito", "audiencia", "objetivo", "alcance", "área"]
    data = {}
    
    for field in fields:
        # Patrón 1: Texto plano -> Propósito: Contenido... (hasta salto de línea doble o siguiente keyword)
        # Patrón 2: JSON sucio -> "propósito": "Contenido...",
        
        # Normalizamos un poco para facilitar la búsqueda
        # Buscamos la clave seguida de : o ":
        pattern = re.compile(rf'(?:^|\n|")\s*{field}\s*(?:"?)\s*:\s*(?:"?)\s*(.*?)(?:(?=\n\s*(?:{"|".join(fields)}))|(?="\s*,)|$)', re.IGNORECASE | re.DOTALL)
        
        match = pattern.search(text)
        if match:
            # Limpiamos comillas finales o comas si se colaron del formato JSON
            content = match.group(1).strip()
            if content.endswith('",'):
                content = content[:-2]
            elif content.endswith('"'):
                content = content[:-1]
            data[field] = content
            
    return data

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
                    "Eres un redactor técnico senior experto en documentación de sistemas y procesos. "
                    "Tu objetivo es redactar una sección introductoria profesional, detallada y bien estructurada para un manual técnico. "
                    "Analiza profundamente el contenido proporcionado y genera descripciones que aporten valor, evitando frases genéricas. "
                    "Responde SIEMPRE en español y SOLO en formato JSON válido. "
                    "El JSON debe contener EXACTAMENTE las siguientes claves: "
                    "'propósito', 'ámbito', 'audiencia', 'objetivo', 'alcance', 'área'. "
                    "\nInstrucciones para cada campo:\n"
                    "- 'propósito': Explica la razón de ser del documento y su utilidad principal.\n"
                    "- 'ámbito': Define el contexto o entorno donde aplica este manual (ej. sistemas, departamentos).\n"
                    "- 'audiencia': Describe el perfil técnico o roles a los que va dirigido.\n"
                    "- 'objetivo': Define la meta concreta que logrará el usuario al seguir este manual.\n"
                    "- 'alcance': Delimita qué cubre y qué no cubre el documento.\n"
                    "- 'área': Indica el departamento o área funcional responsable (ej. Infraestructura, Soporte, Desarrollo).\n"
                    "Usa un tono formal, corporativo y preciso."
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
    print(f"🔍 Respuesta cruda LLM: {raw}")
    match = re.search(r"(\{.*\})", raw, re.DOTALL)
    data = {}

    if match:
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            print("⚠️ Error al decodificar JSON, intentando recuperación por Regex.")
            data = parse_fallback(raw)
    else:
        print("⚠️ No se encontró JSON válido, intentando recuperación por Regex.")
        data = parse_fallback(raw)
    
    print(f"🔍 Datos extraídos (antes de limpieza): {data}")

    return {
        "propósito": data.get("propósito", "").strip(),
        "ámbito": data.get("ámbito", "").strip(),
        "audiencia": data.get("audiencia", "").strip(),
        "objetivo": data.get("objetivo", "").strip(),
        "alcance": data.get("alcance", "").strip(),
        "área": data.get("área", "").strip()
    }
