from ollama import chat
from services.readerService import leer_manual

def generar_titulo():
    """
    Genera un título formal basado en el contenido de Manual.docx.
    Retorna una cadena de texto con el título sugerido.
    """
    try:
        texto_manual = leer_manual()
    except FileNotFoundError:
        print("⚠️ No se encontró templates/Manual.docx. Sube primero un archivo.")
        return "Manual para la documentación técnica"  # valor por defecto

    response = chat(
        model="llama2:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente que SIEMPRE responde en español y que "
                    "únicamente debe generar un título formal para un manual de procedimientos. "
                    "El título debe comenzar con la frase 'Manual para' y describir brevemente el tema del documento. "
                    "No incluyas explicaciones ni signos de puntuación innecesarios; responde solo con el título final."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Dime qué título podría tener este manual, basado en el siguiente contenido:\n\n{texto_manual}"
                ),
            },
        ],
    )

    # Limpiar la respuesta
    titulo = response.message.content.strip()
    if not titulo.lower().startswith("manual para"):
        titulo = "Manual para " + titulo

    return titulo
