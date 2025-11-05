from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from services.manualService import generarManualCompleto

router= APIRouter(prefix="/manual", tags=["Manual"])

ARCHIVO_DIR = Path("archivo_original")

@router.post("/upload")
async def subirGenerarManual(file: UploadFile = File(...)):

    try:
        ARCHIVO_DIR.mkdir(exist_ok=True)

        file_path = ARCHIVO_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        resultado = generarManualCompleto()

        if resultado["status"] == "error" :
            raise HTTPException(status_code=500, detail=resultado["message"])
        
        return{
            "message":"Manual generado exitosamente",
            "file_uploaded" : file.filename,
            "output_path" : resultado["path"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir o procesar el archivo: {str(e)}")
