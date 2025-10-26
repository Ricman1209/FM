# Importa la clase Composer del módulo docxcompose, que permite combinar varios documentos de Word (.docx)
from docxcompose.composer import Composer
# Importa la clase Document de la librería python-docx, usada para abrir, leer y modificar documentos Word
from docx import Document

# Define una función llamada 'unir_documentos' que recibe:
# - ruta_salida: la ruta donde se guardará el documento final unido
# - *ruta_entrada: un número variable de rutas de entrada (los documentos a unir)
def unir_documentos(ruta_salida, *ruta_entrada):

    # Crea el documento base a partir del primer archivo de la lista de entrada    
    doc_base=Document(ruta_entrada[0])
    # Crea un objeto Composer, que usará el documento base como punto de partida para unir los demás
    unificador = Composer(doc_base)
    # Recorre los demás documentos de la lista (empezando desde el segundo)
    for ruta in ruta_entrada[1:]:
        # Abre cada documento individualmente
        documento = Document(ruta)
        # Agrega un salto de página al final del documento base antes de añadir el siguiente
        doc_base.add_page_break()
        # Añade (anexa) el documento actual al documento base
        unificador.append(documento)    
    # Guarda el nuevo documento unificado en la ruta especificada por 'ruta_salida'
    unificador.save(ruta_salida)
    # Imprime un mensaje confirmando que el proceso terminó correctamente
    print(f"Documentos unidos correctamente en {ruta_salida}")


# Bloque principal del script: solo se ejecuta si el archivo se corre directamente (no si es importado)
if __name__ == "__main__":
    # Define el nombre del archivo de salida (el documento final unificado)
    output_file = "documento_unido.docx"
    # Define una lista de archivos de entrada que serán combinados
    input_files = ["doc1.docx", "doc2.docx", "doc3.docx"]
    # Llama a la función 'unir_documentos' pasando los archivos de entrada y el archivo de salida
    # El operador * descompone la lista 'input_files' en argumentos individuales
    unir_documentos(output_file, *input_files)


