# Importamos la clase DocxTemplate de la librería docxtpl
# Esta clase permite trabajar con plantillas de documentos Word (.docx)
# sustituyendo marcadores de texto por valores dinámicos (como {{title}}, {{date}}, etc.)
from docxtpl import DocxTemplate
# Importamos datetime para obtener la fecha actual del sistema
from datetime import datetime
# Importamos Path de la librería pathlib para manejar rutas de archivos de forma segura y multiplataforma
from pathlib import Path



def generar_portada(title: str, output_dir: str = "uploads"):

    """  
      Genera una portada personalizada en formato Word (.docx) usando una plantilla base.

    Parámetros:
        title (str): Título del manual o proyecto que aparecerá en la portada.
        output_dir (str, opcional): Carpeta donde se guardará el archivo generado. 
                                    Por defecto se usa la carpeta 'uploads'.

    Retorna:
        str: Ruta completa del archivo .docx generado.
    """

    #Crear (si no existe) la carpeta donde se guardarán los archivos generados
    path = Path(output_dir)
    #exist_ok=True evita error si la carpeta ya existe
    path.mkdir(exist_ok=True)


    #Cargar la plantilla de Word desde la carpeta 'templates'
    #Esta plantilla debe contener variables como {{Project_name}}, {{date}}, {{versión}}, etc.
    portada_doc = DocxTemplate("templates/portada_manuales_techxagon.docx")

    #Obtener la fecha actual del sistema y formatearla como DD/MM/YYYY
    date = datetime.now()
    date_now = date.strftime("%d/%m/%Y")

    #Definir la versión del documento (puede modificarse si se generan nuevas versiones)
    version = "1.0"

    #Crear un diccionario con las variables que se reemplazarán en la plantilla
    context = {
    'Project_name' : title,
    'date' : date_now,
    'versión' : version
    }
    
    #Definir la ruta de salida final del archivo, combinando la carpeta y el nombre dinámico
    output_path = path / f"Manual para{title}.docx"
    portada_doc.render(context)
    portada_doc.save(output_path)


    return str(output_path)



