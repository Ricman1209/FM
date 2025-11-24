# FM - Generador Automático de Manuales 🚀

Este proyecto es una API REST desarrollada con **FastAPI** diseñada para automatizar la creación de manuales y documentación técnica en formato Word (`.docx`).

## 📋 Características

*   **Generación de Manuales**: Crea documentos completos unificando múltiples secciones.
*   **Integración con IA**: Genera automáticamente secciones introductorias y glosarios de términos utilizando Inteligencia Artificial.
*   **Diagramas Automáticos**: Genera e inserta diagramas de flujo y arquitectura utilizando **Mermaid** y `diagrams`.
*   **Manejo de Archivos**: Soporte para lectura y procesamiento de archivos Word y PDF.
*   **Portadas Personalizadas**: Generación automática de portadas estandarizadas para los manuales.

## 🛠️ Tecnologías

*   **Python 3.x**
*   **FastAPI**: Framework web moderno y rápido.
*   **python-docx / docxtpl**: Manipulación de archivos Word.
*   **PyMuPDF / PyPDF2**: Procesamiento de PDFs.
*   **Mermaid CLI**: Para la generación de imágenes de diagramas.

## ⚙️ Instalación

1.  **Clonar el repositorio**:
    ```bash
    git clone <url-del-repositorio>
    cd FM
    ```

2.  **Crear un entorno virtual**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Linux/Mac
    .venv\Scripts\activate     # En Windows
    ```

3.  **Instalar dependencias de Python**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar dependencias externas**:
    Este proyecto requiere **Mermaid CLI** para la generación de diagramas. Asegúrate de tener Node.js instalado.
    ```bash
    npm install -g @mermaid-js/mermaid-cli
    ```

## 🚀 Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

El servidor se iniciará en `http://127.0.0.1:8000`.

## 📖 Documentación de la API

Una vez iniciado el servidor, puedes acceder a la documentación interactiva generada automáticamente por Swagger UI en:

*   **Swagger UI**: `http://127.0.0.1:8000/docs`
*   **ReDoc**: `http://127.0.0.1:8000/redoc`

## 📂 Estructura del Proyecto

*   `main.py`: Punto de entrada de la aplicación.
*   `routers/`: Definición de endpoints de la API.
*   `services/`: Lógica de negocio (generación de manuales, diagramas, etc.).
*   `utils/`: Utilidades para secciones específicas (portada, glosario).
*   `prompt/`: Prompts y lógica para la generación de texto con IA.
*   `templates/`: Plantillas base para los documentos.
*   `uploads/`: Directorio temporal para archivos generados.

## 🔧 Configuración

Asegúrate de configurar las variables de entorno necesarias creando un archivo `.env` en la raíz del proyecto (basado en el archivo de ejemplo si existe).
