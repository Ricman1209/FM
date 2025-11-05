from pathlib import Path
import os
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.PortadaUtils import generarPortada
from utils.GlosarioUtils import generarGlosario
from utils.SecciónIntroductorioUtils import generarSecciónIntroductoria
from prompt.PromptSecciónIntroductoria import generar_seccion_introductoria
from prompt.PromtGlosario import generar_glosario   # ✅ usa la nueva función

from services.fileService import subir_manual_automatico
from services.mergeService import preparar_y_unir
from services.diagramService import generar_diagrama_mermaid, insertar_diagrama_en_docx


def generarManualCompleto():
    """
    Ejecuta la generación completa del manual:
    1. Copia el documento base a templates/
    2. Genera portada, sección introductoria, glosario y diagrama
    3. Elimina manual previo si existe
    4. Une todo en uploads/manual_final.docx
    """

    try:
        print("🚀 Iniciando generación de manual...\n")

        # 🧹 Si ya existe un manual_final.docx previo, eliminarlo antes de crear el nuevo
        final_path = Path("uploads") / "manual_final.docx"
        if final_path.exists():
            try:
                os.remove(final_path)
                print(f"🧹 Eliminado manual previo: {final_path}")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar el manual previo: {e}")

        # 0️⃣ Asegurar Manual.docx
        subir_manual_automatico()

        # 1️⃣ Portada
        generarPortada()
        print("✅ Portada generada correctamente.\n")

        # 2️⃣ Sección introductoria (usa IA si está disponible)
        try:
            datos_intro = generar_seccion_introductoria()
            if datos_intro:
                generarSecciónIntroductoria(datos_intro)
            else:
                generarSecciónIntroductoria()  # fallback
            print("✅ Sección introductoria generada correctamente.\n")
        except Exception as e:
            print(f"⚠️ Error en sección introductoria: {e}")

        # 3️⃣ Glosario
        try:
            glosario_data = generar_glosario()       # ✅ genera la IA
            generarGlosario(glosario_data)           # ✅ inserta en DOCX
            print("✅ Glosario generado correctamente.\n")
        except Exception as e:
            print(f"⚠️ Error en glosario: {e}")

        # 4️⃣ Diagrama
        try:
            rutaPng = generar_diagrama_mermaid()
            insertar_diagrama_en_docx(rutaPng)
            print("✅ Diagrama generado e insertado correctamente.\n")
        except Exception as e:
            print(f"⚠️ Error en diagrama: {e}")

        # 5️⃣ Unión final
        finalPath = preparar_y_unir()
        print("🎉 Manual completo generado exitosamente en uploads/manual_final.docx")

        return {"status": "success", "path": str(finalPath)}

    except Exception as e:
        print(f"❌ Error durante la generación del manual: {e}")
        return {"status": "error", "message": str(e)}
