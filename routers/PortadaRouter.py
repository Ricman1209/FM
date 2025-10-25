from fastapi import APIRouter, Form
from utils.PortadaUtils import generar_portada

router = APIRouter(prefix="/portada", tags=["La Portada"])

@router.post("/AgregarPortada")
async def generarPortadaDocumento(title:str = Form(...)):
    path = generar_portada(title, output_dir="uploads")
    return{"message" : "Portada agregada", "path":path}
  