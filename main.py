from Services.correo import enviar_correo_con_pdf
from leerRoles import GenerarPdfs
from dotenv import load_dotenv
from pathlib import Path
import os
import time
load_dotenv()
def main():
    print("Script automatizacion ")
    opc=1
    while(opc!=0):
        print("1-Generar pdf")
        print("2-Enviar pdfs")
        opc= int(input("Ingrese un a opcion: "))
        match(opc):
            case 1:
                print("Generando pdfs...")
                GenerarPdfs()
            case 2:
                print("Envio de correos")
                carpeta = "Rol-Octubre-2025"
                for archivo in os.listdir(carpeta):
                    ruta_completa = os.path.join(carpeta, archivo)
                    if os.path.isfile(ruta_completa):
                        nombre, extension = os.path.splitext(archivo)
                    print(f"Nombre: {nombre}, Extensión: {extension}")
                    Nombe_completo=nombre+extension
                    print(enviar_correo_con_pdf(PDF_PATH="./Rol-Octubre-2025/"+Nombe_completo, TO_EMAIL="",TO_NAME="Hola"))
                    time.sleep(2)
                print("Correos Enviados")
if __name__ == "__main__":
    main()