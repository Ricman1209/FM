import io
from PyPDF2 import PdfReader  
from docx import Document


async def extract_text(file):
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith("pdf"):
        pdf = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text.strip()
    
    elif filename.endswith("docx"):
        doc = Document(io.BytesIO(content))
        text = "\n".join(p.text for p in doc.paragraphs)
        return text.strip()
    
    else:
        return"formato no correcto, favor de verificar si es un Word o PDF"
