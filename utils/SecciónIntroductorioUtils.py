from docxtpl import DocxTemplate
from pathlib import Path

def generarSecciónIntroductoria(datos_intro=None):
    doc = DocxTemplate("templates/FormatoSecciónIntroductoria.docx")

    context = {
        "propósito_documento": datos_intro.get("propósito", "Propósito no disponible"),
        "ámbito_documento": datos_intro.get("ámbito", "Ámbito no disponible"),
        "audiencia_documento": datos_intro.get("audiencia", "Audiencia no disponible"),
        "objetivo_documento": datos_intro.get("objetivo", "Objetivo no disponible"),
        "alcance_documento": datos_intro.get("alcance", "Alcance no disponible"),
        "area_documento": datos_intro.get("área", "Área no disponible")
    }

    doc.render(context)
    output_path = Path("uploads") / "FormatoSecciónIntroductoria_automatico.docx"
    doc.save(output_path)
    print(f"✅ Documento generado en: {output_path}")
    return output_path
