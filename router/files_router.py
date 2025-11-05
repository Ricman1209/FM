from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import APIRouter, UploadFile, File
from services.file_service import save_file, delete_file, check_files

router = APIRouter(prefix="/files", tags=["Archivos"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    📤 Endpoint para subir un archivo .docx a archivo_original/
    """
    return await save_file(file)


@router.delete("/delete/{filename}")
async def delete_uploaded_file(filename: str):
    """
    🗑️ Endpoint para eliminar un archivo existente
    """
    return delete_file(filename)


@router.get("/verify")
async def verify_files():
    """
    🔍 Endpoint para verificar si hay archivos en la carpeta
    """
    return check_files()
