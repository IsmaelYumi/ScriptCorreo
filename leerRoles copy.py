import os
import pandas as pd
import fitz  # PyMuPDF


# ================================
# 1) LEER EXCEL Y EL RANGO
# ================================
archivo = "10 OCT 2025 copy.xlsx"
hoja = "OCTUBRE 2025"

df = pd.read_excel(archivo, sheet_name=hoja)

# Rango A8 → BB57
df = df.iloc[4:9, 0:54]

# Asumiendo que la fila 8 tiene encabezados
df.columns = df.iloc[0]
df = df[1:]
df.reset_index(drop=True, inplace=True)


# Eliminar columnas completamente vacías
df = df.dropna(axis=1, how='all')

# Renombrar columnas para quitar espacios y saltos de línea
df.columns = df.columns.astype(str).str.strip()
# ================================
# 2) FUNCION PARA LLENAR EL PDF
# ================================
def llenar_pdf(template_pdf, output_pdf, fila):
    pdf = fitz.open(template_pdf)
    page = pdf[0]
    # EJEMPLO DE CAMPOS — AJUSTA LAS COORDENADAS
    page.insert_text((50, 80),  f"{fila['NOMBRE']}")
    page.insert_text((50, 110), f"{fila['CEDULA']}")
    page.insert_text((50, 140), f"{fila['SUELDO BRUTO']}")
    page.insert_text((50, 170), "Rol Octubre 2025")

    pdf.save(output_pdf)
    pdf.close()


# ================================
# 3) CREAR CARPETA DE SALIDA
# ================================
carpeta = "Rol-Octubre-2025"
os.makedirs(carpeta, exist_ok=True)


# ================================
# 4) GENERAR PDF POR CADA REGISTRO
# ================================
template_pdf = "ROL INDIVIDUAL.pdf"

# Eliminar columnas duplicadas conservando la primera aparición
df = df.loc[:, ~df.columns.duplicated()]

# Eliminar columnas llamadas 'nan'
df = df.loc[:, df.columns != 'nan']

# Normalizar nombres: quitar espacios, saltos de línea y puntos finales
df.columns = (
    df.columns
      .astype(str)
      .str.replace(r'\s+', ' ', regex=True)   # Un solo espacio
      .str.replace('\n', ' ', regex=False)
      .str.replace('.', '', regex=False)      # eliminar puntos del final
      .str.strip()
)

print(df.columns)

for idx, fila in df.iterrows():

    # Validar que existan datos
    if pd.isna(fila["NOMBRE"]) or pd.isna(fila["CEDULA"]):
        print(f"Fila {idx} saltada (datos incompletos).")
        continue

    # Limpiar nombre y cédula para usarlos como nombre de archivo
    nombre = str(fila["NOMBRE"]).replace("/", "-").replace("\\", "-")
    cedula = str(fila["CEDULA"]).replace("/", "-").replace("\\", "-")

    pdf_salida = f"{carpeta}/{nombre}-{cedula}.pdf"
    

    llenar_pdf(template_pdf, pdf_salida, fila)


print("PDFs generados correctamente.")
