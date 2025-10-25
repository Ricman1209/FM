from docxtpl import DocxTemplate
from datetime import datetime
from docx import Document
from pathlib import Path

def generar_portada(title: str, output_dir: str = "uploads"):
    path = Path(output_dir)
    path.mkdir(exist_ok=True)

    portada_doc = DocxTemplate("templates/portada_manuales_techxagon.docx")

    date = datetime.now()
    date_now = date.strftime("%d/%m/%Y")
    version = "1.0"

    context = {
    'Project_name' : title,
    'date' : date_now,
    'versión' : version
    }

    output_path = path / f"Manual para{title}.docx"
    portada_doc.render(context)
    portada_doc.save(output_path)


    return str(output_path)



