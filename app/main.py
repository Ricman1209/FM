from fastapi import FastAPI
from app.routers import documents_router

app = FastAPI(title="FM 0.1", description="Version test para extracción texto en documentos Word")

#registrar rutas 
app.include_router(documents_router.router)

