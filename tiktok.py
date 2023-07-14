import pymongo
import pandas as pd


# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Ejemplo"]

# Nombre de la colección
collection_name = "cuentasTik"

# Obtener la colección
collection = database[collection_name]

# Ruta y nombre del archivo Excel
excel_file = "Análisis Global EC 1_actualizado.xlsx"

# Leer el archivo Excel
df = pd.read_excel(excel_file)

# Iterar sobre los registros del archivo Excel
for _, row in df.iterrows():
    # Obtener el username del campo "Tiktok"
    tiktok_url = row["Tiktok"]
    if isinstance(tiktok_url, str) and tiktok_url.strip() != "":
        at_symbol_index = tiktok_url.rfind("@")
        question_mark_index = tiktok_url.rfind("?")
        if at_symbol_index != -1 and question_mark_index != -1 and question_mark_index > at_symbol_index:
            username = tiktok_url[at_symbol_index + 1:question_mark_index]
        elif at_symbol_index != -1:
            username = tiktok_url[at_symbol_index + 1:]
        elif question_mark_index != -1:
            username = tiktok_url[:question_mark_index]
        else:
            username = tiktok_url

        # Filtrar el documento por el campo "username"
        documento = collection.find_one({"username": username})

        # Verificar si se encontró un documento
        if documento:
            # Hacer una copia del documento sin el campo _id
            copia = documento.copy()
            itemId = documento.get('_id')
            copia.pop('_id', None)

            # Realizar las modificaciones en el documento
            copia["contextA"] = row["Contexto del Medio"].capitalize()

            tipo_medio = row["Tipo del Medio"]
            if isinstance(tipo_medio, str):
                copia["typeA"] = tipo_medio.capitalize()
            else:
                copia["typeA"] = tipo_medio

            copia["country"] = row["PAÍS"].capitalize()
            copia["region"] = row["REGIÓN"].capitalize()
            copia["province"] = row["PROVINCIA"].capitalize()
            copia["city"] = row["CIUDAD"].capitalize()
            copia["parish"] = row["PARROQUIA"]

            # Actualizar el documento en MongoDB
            filter = {"_id": itemId}
            collection.update_one(filter, {"$set": copia})

            # Mostrar mensaje de actualización
            print(f"Documento actualizado: {username}")

        else:
            # Mostrar mensaje de columna "Tiktok" vacía
            print(f"Columna 'Tiktok' vacía para el username: {username}")

# Cerrar la conexión a MongoDB
client.close()
