from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importar solo esta función primero (para preparar Manual.docx)
from utils.SubirManualUtils import subir_manual_automatico


def main():
    print("🚀 Iniciando generación automática de manual...\n")

    # 0️⃣ Copiar el último archivo de archivo_original/ a templates/Manual.docx
    try:
        subir_manual_automatico()
    except Exception as e:
        print(f"❌ Error al preparar el documento base: {e}")
        return

    # ✅ Solo después de tener Manual.docx, importamos los demás módulos
    from utils.PortadaUtils import generarPortada
    from utils.GlosarioUtils import generarGlosario
    from utils.SecciónIntroductorioUtils import generarSecciónIntroductoria
    from utils.UnirDocumentosUtils import preparar_y_unir

    # 1️⃣ Generar portada
    generarPortada()
    print("✅ Portada generada correctamente.\n")

    # 2️⃣ Generar sección introductoria
    generarSecciónIntroductoria()
    print("✅ Sección introductoria generada correctamente.\n")

    # 3️⃣ Generar glosario
    generarGlosario()
    print("✅ Glosario generado correctamente.\n")

    # 4️⃣ Unir todo
    preparar_y_unir()
    print("\n🎉 Manual completo generado exitosamente en 'uploads/manual_final.docx'")


if __name__ == "__main__":
    main()
