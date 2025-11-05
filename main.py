from fastapi import FastAPI
from routers.manualRouter import router as manual_router

app = FastAPI(title="FM API")

app.include_router(manual_router)

@app.get("/")
def root():
    return {"message": "🚀 Servidor FM corriendo correctamente"}
