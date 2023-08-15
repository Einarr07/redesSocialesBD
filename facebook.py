import pymongo
import pandas as pd

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Ejemplo"]
collection_name = "cuentasFace"
collection = database[collection_name]

# Ruta y nombre del archivo Excel
excel_file = "Cuentas RD.xlsx"

# Nombre de la hoja en el archivo Excel
excel_sheet_name = "Facebook"

# Leer la hoja de cálculo "Facebook" del archivo Excel
df = pd.read_excel(excel_file, sheet_name=excel_sheet_name)

for _, row in df.iterrows():
    cuenta = row[1]
    region = row[2]
    subregion = row[3]
    provincia = row[4]
    municipio = row[5]

    filter = {"name": cuenta}
    documento = collection.find_one(filter)

    if documento:
        copia = documento.copy()
        itemId = documento.get('_id')
        copia.pop('_id', None)

        #Realizar las modificaciones en el documento
        copia["region"] = region
        copia["subRegion"] = subregion
        copia["prov"] = provincia
        copia["city"] = municipio

        #Actualizar el documento en Mongo DB
        filter = {"_id": itemId}
        collection.update_one(filter, {"$set": copia})
        print(f"Documento actualizado: {cuenta}")
    else:
        print(f"No se encontró un documento para la cuenta: {cuenta}")

# Cerrar la conexión a MongoDB
client.close()
