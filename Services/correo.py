import os
from mailjet_rest import Client
import base64
from dotenv import load_dotenv

load_dotenv()

# ==========================
# CONFIGURACIÓN DE MAILJET
# ==========================
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("SECRET_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "RRHH") 
def enviar_correo_con_pdf(PDF_PATH, TO_EMAIL, TO_NAME):
    # Crear cliente de Mailjet
    mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')
    # Leer PDF y convertirlo a base64
    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()
        pdf_b64 = base64.b64encode(pdf_bytes).decode()

    # Cuerpo del correo
    data = {
        'Messages': [
            {
                "From": {
                    "Email": FROM_EMAIL,
                    "Name": FROM_NAME
                },
                "To": [
                    {
                        "Email": TO_EMAIL,
                        "Name": TO_NAME
                    }
                ],
                "Subject": "Tu PDF está listo ✔",
                "TextPart": "Adjunto el archivo PDF que solicitaste.",
                "Attachments": [
                    {
                        "ContentType": "application/pdf",
                        "Filename": "Rol de pago.pdf",
                        "Base64Content": pdf_b64
                    }
                ]
            }
        ]
    }
    # Enviar correo
    result = mailjet.send.create(data=data)
    return result