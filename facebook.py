import pymongo
import pandas as pd


# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Ejemplo"]

# Nombre de la colección
collection_name = "cuentasFace"

# Obtener la colección
collection = database[collection_name]

# Ruta y nombre del archivo Excel
excel_file = "Análisis Global EC 1_actualizado.xlsx"

# Leer el archivo Excel
df = pd.read_excel(excel_file)

# Iterar sobre los registros del archivo Excel
for _, row in df.iterrows():
    # Obtener el username del campo "Facebook"
    facebook_url = row["Facebook"]
    if isinstance(facebook_url, str) and facebook_url.strip() != "":
        last_slash_index = facebook_url.rfind("/")
        if last_slash_index != -1:
            username = facebook_url[last_slash_index + 1:]
        else:
            username = facebook_url

        # Filtrar el documento por el campo "username"
        filter = {"username": username}

        # Buscar el documento por el username en MongoDB
        documento = collection.find_one(filter)

        # Verificar si se encontró un documento
        if documento:
            # Hacer una copia del documento sin el campo _id
            copia = documento.copy()
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
            collection.update_one(filter, {"$set": copia})

            # Mostrar mensaje de actualización
            print(f"Documento actualizado: {username}")

        else:
            # Mostrar mensaje de columna "Facebook" vacía
            print(f"Columna 'Facebook' vacía para el username: {username}")

# Cerrar la conexión a MongoDB
client.close()
