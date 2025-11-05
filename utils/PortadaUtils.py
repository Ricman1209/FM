from docxtpl import DocxTemplate
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.PromptTitulo import generar_titulo


def generarPortada():
    """
    Genera la portada del manual automáticamente.
    Usa el título generado por la IA (Ollama) y la fecha actual.
    """
    try:
        doc = DocxTemplate("templates/portada_manuales_techxagon.docx")

        # Generar título dinámico con IA
        titulo = generar_titulo()

        # Contexto para la plantilla
        context = {
            "Project_name": titulo,
            "date": datetime.now().strftime("%d/%m/%Y"),
            "versión": "1.0",
        }

        # Renderizar plantilla
        doc.render(context)
        output_path = Path("uploads") / "portada_automatica.docx"
        doc.save(output_path)

        print(f"✅ Portada generada en: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error al generar portada: {e}")
        return None
