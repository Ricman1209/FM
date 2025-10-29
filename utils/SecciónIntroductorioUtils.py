from docxtpl import DocxTemplate
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.PromptSecciónIntroductoria import Propósito, Ámbito, Audiencia
from prompt.PromptSecciónIntroductoria import Objetivo, Alcance, Área

def generarSecciónIntroductoria():
    doc = DocxTemplate("templates/FormatoSecciónIntroductoria.docx")

    context = {
        "propósito_documento" : Propósito,
        "ámbito_documento" : Ámbito,
        "audiencia_documento" : Audiencia,
        "objetivo_documento" : Objetivo,
        "alcance_documento" : Alcance,
        "area_documento" : Área
    }

    doc.render(context)
    doc.save("uploads/FormatoSecciónIntroductoria_automatico.docx")

if __name__ == "__main__":
    print("🧩 Generando sección introductoria...")
    generarSecciónIntroductoria()
    print("✅ Documento generado en: uploads/FormatoSecciónIntroductoria_automatico.docx")
