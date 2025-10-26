

Title = "titulo_ejemplo_desde_promt/portadaPrompt.py"



def obtener_glosario_desde_api():
    """
    Simula la consulta a una API que devuelve un glosario con varios términos.
    En un caso real podrías usar: response = requests.get("https://miapi.com/glosario")
    """
    glosario_api = [
        {"termino": "API", "significado": "Interfaz que permite la comunicación entre aplicaciones."},
        {"termino": "Servidor", "significado": "Equipo que provee servicios o recursos a otros dispositivos en red."},
        {"termino": "Cliente", "significado": "Aplicación o dispositivo que solicita servicios al servidor."},
        {"termino": "Endpoint", "significado": "Punto de acceso de una API donde se reciben o envían solicitudes."},
        {"termino": "JSON", "significado": "Formato de texto ligero para el intercambio de datos estructurados."}
    ]
    return glosario_api


