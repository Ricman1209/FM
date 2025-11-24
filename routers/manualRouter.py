from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
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

@router.get("/download")
async def descargar_manual():
    try:
        file_path = Path("uploads/manual_final.docx")
        if not file_path.exists():
            # Intentar con ruta absoluta si la relativa falla
            base_path = Path(__file__).resolve().parent.parent
            file_path = base_path / "uploads" / "manual_final.docx"
            
        if not file_path.exists():
             raise HTTPException(status_code=404, detail="El archivo manual_final.docx no se encuentra en uploads")

        return FileResponse(
            path=file_path, 
            filename="manual_final.docx", 
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el archivo: {str(e)}")
