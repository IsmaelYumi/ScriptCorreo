import smtplib
import os
import logging
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Configurar logger
logger = logging.getLogger(__name__)

load_dotenv()

# CONFIGURACIÓN SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL = os.getenv("Email")
PASSWORD = os.getenv("Clave")

class EmailError(Exception):
    """Excepción personalizada para errores de email"""
    pass

def validar_configuracion():
    if not EMAIL or not PASSWORD:
        raise EmailError("Faltan credenciales: configura EMAIL y Clave en variables de entorno")
    return True

def enviar_correo(
    destinatario: str,
    asunto: str,
    mensaje: str,
    ruta_pdf: str = None,
    html: bool = False,
    attachments: list = None
):
    try:
        # Validar configuración
        validar_configuracion()
        
        # Validar destinatario
        if not destinatario or "@" not in destinatario:
            raise EmailError(f"Destinatario inválido: {destinatario}")
        
        # Crear mensaje
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL
        msg["To"] = destinatario
        msg["Subject"] = asunto
        
        # Adjuntar cuerpo del mensaje
        mime_type = "html" if html else "plain"
        msg.attach(MIMEText(mensaje, mime_type, "utf-8"))
        
        # Procesar adjuntos
        archivos_adjuntar = []
        
        # Retrocompatibilidad: agregar ruta_pdf si existe
        if ruta_pdf:
            archivos_adjuntar.append(ruta_pdf)
        
        # Agregar otros adjuntos
        if attachments:
            archivos_adjuntar.extend(attachments)
        
        # Adjuntar archivos
        for ruta in archivos_adjuntar:
            if not ruta:
                continue
                
            archivo_path = Path(ruta)
            
            if not archivo_path.exists():
                logger.warning(f"Archivo no encontrado: {ruta}")
                continue
            
            # Determinar tipo MIME basado en extensión
            extension = archivo_path.suffix.lower()
            maintype = "application"
            subtype = {
                ".pdf": "pdf",
                ".jpg": "jpeg",
                ".jpeg": "jpeg",
                ".png": "png",
                ".txt": "plain",
                ".csv": "csv",
                ".xlsx": "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }.get(extension, "octet-stream")
            
            # Leer y adjuntar archivo
            with open(archivo_path, "rb") as f:
                parte = MIMEBase(maintype, subtype)
                parte.set_payload(f.read())
            
            encoders.encode_base64(parte)
            parte.add_header(
                "Content-Disposition",
                f"attachment; filename={archivo_path.name}"
            )
            msg.attach(parte)
            logger.info(f"Adjunto agregado: {archivo_path.name}")
        
        # Enviar correo
        logger.info(f"Conectando a {SMTP_SERVER}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.set_debuglevel(0)  # Cambiar a 1 para debug
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Correo enviado exitosamente a {destinatario}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "Error de autenticación SMTP. Verifica EMAIL y Clave"
        logger.error(error_msg)
        raise EmailError(error_msg)
    
    except smtplib.SMTPException as e:
        error_msg = f"Error SMTP: {str(e)}"
        logger.error(error_msg)
        raise EmailError(error_msg)
    
    except FileNotFoundError as e:
        error_msg = f"Archivo no encontrado: {str(e)}"
        logger.error(error_msg)
        raise EmailError(error_msg)
    
    except Exception as e:
        error_msg = f"Error inesperado al enviar correo: {str(e)}"
        logger.exception(error_msg)
        raise EmailError(error_msg)

# Función legacy para retrocompatibilidad
def enviar_correo_simple(destinatario: str, asunto: str, mensaje: str, ruta_pdf: str = ""):
    return enviar_correo(destinatario, asunto, mensaje, ruta_pdf)