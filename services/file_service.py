from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import os
from fastapi import UploadFile, HTTPException

# Ruta base a la carpeta donde se almacenan los archivos
BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVO_ORIGINAL_DIR = BASE_DIR / "archivo_original"
ARCHIVO_ORIGINAL_DIR.mkdir(exist_ok=True)


async def save_file(file: UploadFile):
    """
    Guarda un archivo en archivo_original/. Si ya existe, lo reemplaza.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos .docx")

    file_path = ARCHIVO_ORIGINAL_DIR / file.filename
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"message": f"Archivo '{file.filename}' subido correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {e}")


def delete_file(filename: str):
    """
    Elimina un archivo específico dentro de archivo_original/.
    """
    file_path = ARCHIVO_ORIGINAL_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="El archivo no existe.")

    try:
        os.remove(file_path)
        return {"message": f"Archivo '{filename}' eliminado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar archivo: {e}")


def check_files():
    """
    Verifica si existen archivos en archivo_original/ y los lista.
    """
    files = [f.name for f in ARCHIVO_ORIGINAL_DIR.iterdir() if f.is_file()]
    if not files:
        return {"status": "vacio", "message": "No hay documentos en la carpeta."}
    return {"status": "ok", "archivos": files}
