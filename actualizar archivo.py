import pandas as pd

# Ruta del archivo Excel original
archivo_excel = "Análisis Global EC 1.xlsx"

# Ruta del nuevo archivo Excel donde se guardarán los cambios
nuevo_archivo_excel = "Análisis Global EC 1_actualizado.xlsx"

# Leer el archivo Excel original
excel = pd.ExcelFile(archivo_excel)

# Nombre de la hoja de Excel donde se encuentra la información
hoja_excel = "Cuentas por Red Social"

# Leer la hoja de Excel
df = pd.read_excel(archivo_excel, sheet_name=hoja_excel)

# Reemplazar las celdas que contienen "_____" por un valor vacío ("")
df.loc[df["PARROQUIA"] == "_____", "PARROQUIA"] = ""

# Guardar los cambios en un nuevo archivo Excel
df.to_excel(nuevo_archivo_excel, sheet_name=hoja_excel, index=False)

print("Contenido igual a '_____' en la columna 'Parroquia' eliminado correctamente. Se ha creado un nuevo archivo Excel con los cambios: Análisis Global EC 1 Modificado.xlsx.")
