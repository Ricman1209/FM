from docxtpl import DocxTemplate
import jinja2
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.PromtGlosario import Glosario

def generarGlosario():
    doc = DocxTemplate("templates/FormatoGlosario.docx")

    context = {
        "glosario": Glosario
    }

    doc.render(context)
    doc.save("uploads/glosario_automatico.docx")

generarGlosario()

