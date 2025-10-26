from docxtpl import DocxTemplate
import jinja2

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.prompts_ejemplo import obtener_glosario_desde_api


def generarGlosario():
    doc = DocxTemplate("templates/FormatoGlosario.docx")
    glosario_data=obtener_glosario_desde_api()

    context = {
        "glosario":glosario_data
    }

    doc.render(context)
    doc.save("uploads/glosario_generated.docx")


generarGlosario()
