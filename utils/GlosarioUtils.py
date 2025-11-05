from docxtpl import DocxTemplate
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompt.PromtGlosario import generar_glosario  # ✅ función, no variable


def generarGlosario(glosario_data=None):
    """
    Genera un archivo Word con el glosario.
    Si no se pasa glosario_data, lo genera automáticamente con IA.
    """
    try:
        # Si no se pasa un glosario, lo genera con la IA
        if glosario_data is None:
            glosario_data = generar_glosario()

        if not glosario_data:
            print("⚠️ No se generó ningún glosario.")
            return None

        # Cargar la plantilla
        doc = DocxTemplate("templates/FormatoGlosario.docx")

        # Contexto para la plantilla
        context = {
            "glosario": glosario_data
        }

        # Render y guardado
        output_path = Path("uploads/glosario_automatico.docx")
        doc.render(context)
        doc.save(output_path)

        print(f"✅ Glosario generado correctamente en {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error al generar el glosario: {e}")
        return None


if __name__ == "__main__":
    generarGlosario()
