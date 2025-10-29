from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import shutil
import glob
import os

def subir_manual_automatico():
    """
    Busca el último archivo .docx en 'archivo_original/' y lo copia a 'templates/Manual.docx'.
    Sobrescribe si ya existe.
    Devuelve la ruta del nuevo Manual.docx.
    """

    carpeta_origen = Path("archivo_original")
    carpeta_destino = Path("templates")

    # Crear carpetas si no existen
    carpeta_origen.mkdir(parents=True, exist_ok=True)
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    # Buscar archivos .docx en archivo_original/
    archivos = sorted(
        glob.glob(str(carpeta_origen / "*.docx")),
        key=os.path.getmtime,
        reverse=True
    )

    if not archivos:
        raise FileNotFoundError("❌ No hay ningún archivo .docx en 'archivo_original/'")

    # Tomar el más reciente
    archivo_reciente = Path(archivos[0])

    # Copiarlo a templates/Manual.docx (sobrescribir si existe)
    destino = carpeta_destino / "Manual.docx"
    shutil.copy2(archivo_reciente, destino)

    print(f"📂 Archivo original encontrado: {archivo_reciente.name}")
    print(f"✅ Copiado y renombrado como: {destino}")

    return destino


if __name__ == "__main__":
    subir_manual_automatico()
