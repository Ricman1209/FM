from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
import os
from prompt.PromptDiagrama import titulo_diagrama, pasos_diagrama


def generar_diagrama_mermaid():
    """
    Genera un diagrama de flujo con Mermaid a partir de los datos de PromptDiagrama.py.
    Crea un archivo .mmd, lo convierte a .png y luego elimina el .mmd temporal.
    """

    if not pasos_diagrama or len(pasos_diagrama) == 0:
        print("⚠️ No se detectaron pasos en el diagrama.")
        return None

    # 1️⃣ Crear contenido Mermaid dinámico
    contenido = "flowchart TD\n"
    contenido += f'    A[Inicio] --> B["{pasos_diagrama[0]}"]\n'

    for i in range(1, len(pasos_diagrama)):
        letra_anterior = chr(66 + (i - 1))
        letra_actual = chr(66 + i)
        contenido += f'    {letra_anterior}["{pasos_diagrama[i-1]}"] --> {letra_actual}["{pasos_diagrama[i]}"]\n'

    contenido += f'    {chr(66 + len(pasos_diagrama) - 1)} --> Z[Fin]\n'

    # 2️⃣ Definir rutas
    ruta_base = Path("uploads")
    ruta_base.mkdir(exist_ok=True)
    nombre_base = titulo_diagrama.replace(" ", "_")
    ruta_mmd = ruta_base / f"diagrama_{nombre_base}.mmd"
    ruta_png = ruta_base / f"diagrama_{nombre_base}.png"

    # Guardar .mmd
    with open(ruta_mmd, "w", encoding="utf-8") as f:
        f.write(contenido)
    #print(f"📄 Archivo Mermaid generado: {ruta_mmd}")

    # 3️⃣ Ruta absoluta del ejecutable mmdc.cmd
    ruta_mmdc = r"C:\Users\moral\AppData\Roaming\npm\mmdc.cmd"

    if not Path(ruta_mmdc).exists():
        print("❌ No se encontró el ejecutable mmdc.cmd.")
        print("➡️ Ejecuta: npm install -g @mermaid-js/mermaid-cli")
        return None

    # 4️⃣ Ejecutar el comando a través de cmd.exe
    try:
        comando = [
            "cmd", "/c",
            ruta_mmdc, "-i", str(ruta_mmd), "-o", str(ruta_png)
        ]
        subprocess.run(comando, check=True)
        #print(f"✅ Imagen PNG generada: {ruta_png}")

    except subprocess.CalledProcessError as e:
        print("❌ Error al generar el diagrama con Mermaid CLI:", e)
        return None
    except FileNotFoundError:
        print("❌ No se encontró el ejecutable mmdc.cmd.")
        return None

    # 5️⃣ Eliminar el archivo .mmd temporal
    try:
        os.remove(ruta_mmd)
        #print(f"🗑️ Archivo temporal eliminado: {ruta_mmd.name}")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar el archivo temporal: {e}")

    return ruta_png


if __name__ == "__main__":
    generar_diagrama_mermaid()
