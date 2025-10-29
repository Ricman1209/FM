from docx import Document
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from ollama import chat

def leer_manual():
    file_path = Path(__file__).resolve().parent.parent / 'templates' / 'Manual.docx'

    doc = Document(file_path)

    contenido = ""
    for paragraph in doc.paragraphs:
        contenido += paragraph.text + "\n"

    return contenido

manual_text = leer_manual()
#print(manual_text)