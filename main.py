from Services.correo import enviar_correo
from dotenv import load_dotenv
load_dotenv()

def main():
    enviar_correo("yumipantaismael@gmail.com","prueba","queloque","./CV.PDF")
    print()

if __name__ == "__main__":
    main()