from fastapi import FastAPI
from routers import PortadaRouter

app = FastAPI(
    title="Generador de Manuales",
    description="Api para generar el formato correcto a un documentación word básica",
    version="0.1"
)

app.include_router(PortadaRouter.router)

@app.get("/")
def root():
    return{"message":"Api lista"}
