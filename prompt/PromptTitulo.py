from ollama import chat
from utils.LeerDocumento import leer_manual


texto_manual = leer_manual()


response = chat(
    model="llama2:7b",
    messages=[
        {
            "role": "system",
            "content": (
                "Eres un asistente que SIEMPRE responde en español y que "
                "únicamente debe generar un título formal para un manual de procedimientos. "
                "El título debe comenzar con la frase 'Manual para' y describir brevemente el tema del documento. "
                "No incluyas explicaciones ni signos de puntuación innecesarios, responde solo con el título final."
            )
        },
        {
            "role": "user",
            "content": f"dime que titulo le podria poner a este manual:\n\n{texto_manual}"
        }
    ]
)

Title = response.message.content