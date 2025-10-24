from docxtpl import DocxTemplate
from datetime import datetime

doc = DocxTemplate("my_word_template.docx")
context = {'company name' : "World Company"}

#--------------------------------------------
title=input("Escribe el nombre del manual: ")
# DEBERA RECIBIR EL INPUTO DE LA IA
#--------------------------------------------
date = datetime.now()
date_now = date.strftime("%d/%m/%Y")
version = "1.0"

context = {
    'Project_name' : title,
    'date' : date_now,
    'versión' : version

}

doc.render(context)
doc.save("doc con formato.docx")

