from docx import Document
from pathlib import Path

def leer_manual():
    """
    Lee el contenido del archivo templates/Manual.docx
    y devuelve todo el texto como una cadena de texto.
    """
    file_path = Path(__file__).resolve().parent.parent / 'templates' / 'Manual.docx'

    if not file_path.exists():
        raise FileNotFoundError("⚠️ templates/Manual.docx no existe todavía. Sube un archivo antes de intentar leerlo.")

    doc = Document(file_path)
    contenido = ""
    for paragraph in doc.paragraphs:
        contenido += paragraph.text + "\n"

    return contenido
    