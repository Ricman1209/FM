from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.PortadaUtils import generarPortada
from utils.GlosarioUtils import generarGlosario
from utils.SecciónIntroductorioUtils import generarSecciónIntroductoria
from utils.UnirDocumentosUtils import preparar_y_unir


def main():
    print("🚀 Iniciando generación automática de manual...")

    # 1️⃣ Generar portada
    generarPortada()
    print("✅ Portada generada correctamente.")

    # 2️⃣ Generar sección introductoria
    generarSecciónIntroductoria()
    print("✅ Sección introductoria generada correctamente.")

    # 3️⃣ Generar glosario
    generarGlosario()
    print("✅ Glosario generado correctamente.")

    # (Opcional: futuras funciones)
    # generarControlCambios()
    # generarDiagrama()
    # generarÍndice()

    # 4️⃣ Unir todos los documentos en orden y limpiar archivos temporales
    preparar_y_unir()

    print("🎉 Manual completo generado exitosamente en 'uploads/manual_final.docx'")


if __name__ == "__main__":
    main()
