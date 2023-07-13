import pymongo
import pandas as pd
from urllib.parse import urlparse

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Ejemplo"]

# Nombre de la colección
collection_name = "cuentasInsta"

# Obtener la colección
collection = database[collection_name]

# Ruta y nombre del archivo Excel
excel_file = "Análisis Global EC 1_actualizado.xlsx"

# Leer el archivo Excel
df = pd.read_excel(excel_file)

# Iterar sobre los registros del archivo Excel
for _, row in df.iterrows():
    # Obtener el enlace de Instagram
    instagram_url = row["Instagram"]

    # Verificar si el enlace es válido
    if isinstance(instagram_url, str) and instagram_url.strip() != "":
        # Obtener el nombre de usuario del enlace
        parsed_url = urlparse(instagram_url)
        path = parsed_url.path.strip("/")
        parts = path.split("/")
        username = parts[0]

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
            collection.replace_one(filter, copia)

            # Mostrar mensaje de actualización
            print(f"Documento actualizado en la colección 'cuentasInsta' para el username: {username}")

        else:
            # Mostrar mensaje de usuario no encontrado
            print(f"El usuario con el username '{username}' no se encontró en la colección 'cuentasInsta'")

# Cerrar la conexión a MongoDB
client.close()
