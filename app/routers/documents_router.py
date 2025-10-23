from fastapi import File, UploadFile, APIRouter
from app.utils.reader_utils import extract_text

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    sube un archivo docx y extrae su contenido en texto plano
    """
    text = await extract_text(file)
    return {"filename":file.filename,"content": text}

