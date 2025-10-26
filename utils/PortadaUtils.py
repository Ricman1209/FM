from docxtpl import DocxTemplate
import jinja2
from datetime import datetime

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.portadaPrompt import Title



doc = DocxTemplate("templates/portada_manuales_techxagon.docx")


context = {
    "Project_name" : Title,
    "date" : datetime.now().strftime(format="%d/%m/%Y"),
    "versión" : "1.0"
}

jinja2_env = jinja2.Environment(autoescape=True)
doc.render(context , jinja2_env)
doc.save("templates/nuevoword.docx")


