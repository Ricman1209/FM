from docxtpl import DocxTemplate
import jinja2
from datetime import datetime

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.prompts_ejemplo import Title

def generarPortada():
    doc = DocxTemplate("templates/portada_manuales_techxagon.docx")


    context = {
    "Project_name" : Title,
    "date" : datetime.now().strftime(format="%d/%m/%Y"),
    "versión" : "1.0"
    }


    doc.render(context)
    doc.save("templates/word_portada_funcion.docx")

generarPortada()


