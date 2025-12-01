import os
import pandas as pd
import fitz  # PyMuPDF

# ================================
# 1) LEER EXCEL Y EL RANGO
# ================================
archivo = "10 OCT 2025 copy.xlsx"
hoja = "OCTUBRE 2025"

df = pd.read_excel(archivo, sheet_name=hoja)

df = df.iloc[4:9, 0:54]
df.columns = df.iloc[0]
df = df[1:]
df.reset_index(drop=True, inplace=True)
df = df.dropna(axis=1, how='all')
df.columns = df.columns.astype(str).str.strip()

# ================================
# 2) FUNCIÓN PARA LLENAR EL PDF
# ================================
def llenar_pdf(template_pdf, output_pdf, fila):

    pdf = fitz.open(template_pdf)
    page = pdf[0]

    page.insert_text((139, 160), f"{fila['NOMBRE']}",
                    fontname="Aparajita",
                    fontfile="aparaj.ttf",
                    fontsize=10)

    page.insert_text((142, 144), f"{fila['CEDULA']}",
                    fontname="Aparajita",
                    fontfile="aparaj.ttf",
                    fontsize=10)

    page.insert_text((247, 213), f"{fila['SUELDO BRUTO']}",
                    fontname="Aparajita",
                    fontfile="aparaj.ttf",
                    fontsize=10)

    page.insert_text((419, 117), "Rol Octubre 2025",
                    fontname="Aparajita",
                    fontfile="aparaj.ttf",
                    fontsize=10)


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

df = df.loc[:, ~df.columns.duplicated()]
df = df.loc[:, df.columns != 'nan']
df.columns = (
    df.columns
      .astype(str)
      .str.replace(r'\s+', ' ', regex=True)
      .str.replace('\n', ' ', regex=False)
      .str.replace('.', '', regex=False)
      .str.strip()
)

print(df.columns)

for idx, fila in df.iterrows():
    if pd.isna(fila["NOMBRE"]) or pd.isna(fila["CEDULA"]):
        print(f"Fila {idx} saltada (datos incompletos).")
        continue

    nombre = str(fila["NOMBRE"]).replace("/", "-").replace("\\", "-")
    cedula = str(fila["CEDULA"]).replace("/", "-").replace("\\", "-")

    pdf_salida = f"{carpeta}/{nombre}-{cedula}.pdf"

    llenar_pdf(template_pdf, pdf_salida, fila)


print("PDFs generados correctamente.")
