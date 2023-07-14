import pymongo
import pandas as pd
from urllib.parse import urlparse

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Ejemplo"]

# Nombre de la colección
collection_name = "cuentasTwit"

# Obtener la colección
collection = database[collection_name]

# Ruta y nombre del archivo Excel
excel_file = "Análisis Global EC 1_actualizado.xlsx"

# Leer el archivo Excel
df = pd.read_excel(excel_file)

# Iterar sobre los registros del archivo Excel
for _, row in df.iterrows():
    # Obtener el username del campo "Twitter"
    twitter_url = row["Twitter"]
    if isinstance(twitter_url, str) and twitter_url.strip() != "":
        at_symbol_index = twitter_url.rfind("@")
        if at_symbol_index != -1:
            screen_name = twitter_url[at_symbol_index + 1:]
        else:
            parsed_url = urlparse(twitter_url)
            path = parsed_url.path.strip("/")
            parts = path.split("/")
            username = parts[0]
            screen_name = username

            # Omitir todo lo que está después del símbolo "?"
            screen_name_url = parsed_url._replace(query="").geturl()
            screen_name = screen_name_url.split("/")[-1]

        # Filtrar el documento por el campo "screenName"
        #filter = {"_id": itemId}

        # Buscar el documento por el screenName en MongoDB
        documento = collection.find_one({"screenName": screen_name})

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
            print(f"Documento actualizado: {screen_name}")

        else:
            # Mostrar mensaje de columna "Twitter" vacía
            print(f"Columna 'Twitter' vacía para el screenName: {screen_name}")

# Cerrar la conexión a MongoDB
client.close()
