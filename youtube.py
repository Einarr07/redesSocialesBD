import pymongo
import pandas as pd
from urllib.parse import urlparse

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Ejemplo"]

# Nombre de la colección
collection_name = "cuentasYout"

# Obtener la colección
collection = database[collection_name]

# Ruta y nombre del archivo Excel
excel_file = "Análisis Global EC 1_actualizado.xlsx"

# Leer el archivo Excel
df = pd.read_excel(excel_file)

# Iterar sobre los registros del archivo Excel
for _, row in df.iterrows():
    # Obtener el enlace de YouTube
    youtube_url = row["YouTube"]

    # Verificar si el enlace es válido
    if isinstance(youtube_url, str) and youtube_url.strip() != "":
        last_slash_index = youtube_url.rfind("/")
        if last_slash_index != -1:
            userName = youtube_url[last_slash_index + 1:]
            query_index = userName.find("?")
            if query_index != -1:
                if "@" in query_index:
                    userName = userName[:query_index].lower()
                else:
                    userName = query_index
        else:
            if "@" in youtube_url:
                userName = youtube_url.lower()
            else:
                userName = youtube_url

        # Filtrar el documento por el campo "userName"
        # filter = {"userName": userName}

        # Buscar el documento por el userName en MongoDB
        documento = collection.find_one({"$or": [{"userName": userName}, {"_id": userName}]})

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
            copia["province"] = str(row["PROVINCIA"]).capitalize()  # Convertir a cadena de texto
            copia["city"] = str(row["CIUDAD"]).capitalize()
            copia["parish"] = row["PARROQUIA"]

            # Actualizar el documento en MongoDB
            filter = {"_id": itemId}
            collection.update_one(filter, {"$set": copia})

            # Mostrar mensaje de actualización
            print(f"Documento actualizado en la colección 'cuentasYout' para el username: {userName}")

        else:
            # Mostrar mensaje de usuario no encontrado
            print(f"El usuario con el username '{userName}' no se encontró en la colección 'cuentasYout'")

# Cerrar la conexión a MongoDB
client.close()
