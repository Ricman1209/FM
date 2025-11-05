from fastapi import FastAPI
import subprocess
from pathlib import Path
import sys
from router.files_router import router as files_router

sys.path.append(str(Path(__file__).resolve().parent.parent))


app = FastAPI(title="FM API")

@app.post("/procesar_doc")
def procesar_doc():
    """
    Endpoint maestro: ejecuta main.py completo.
    """
    try:
        # Ejecuta tu script como un proceso hijo
        subprocess.run(["python", "main.py"], check=True)
        return {"status": "success", "message": "Manual generado correctamente"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "details": str(e)}

app.include_router(files_router)


