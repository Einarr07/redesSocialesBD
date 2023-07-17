import pandas as pd
from pymongo import MongoClient

from credentials import mongoCredentials
from utils import myCapitalize

# Conexión a MongoDB
client = MongoClient(
    host=mongoCredentials.get("host"),
    port=mongoCredentials.get("port"),
    username=mongoCredentials.get("username"),
    password=mongoCredentials.get("password"),
    authSource=mongoCredentials.get("authSource"),
    authMechanism=mongoCredentials.get("authMechanism")
)
database = client["qliksocial"]
# Nombre de la colección
collection_name = "cfgTw_BK"
# Obtener la colección
collection = database[collection_name]
# Ruta y nombre del archivo Excel
excel_file = "Análisis Global EC 1_actualizado.xlsx"
# Leer el archivo Excel
df = pd.read_excel(excel_file)

# Iterar sobre los registros del archivo Excel
for _, row in df.iterrows():
    # Obtener el username del campo "Twitter"
    myUrl = row["Twitter"]
    fullUrl = myUrl
    if isinstance(myUrl, str) and myUrl.strip() != "":
        screen_names = []
        myUrl = myUrl.strip()
        myUrl = myUrl.split(".com/")[-1]
        if "/" in myUrl:
            myUrl = myUrl.split("/")[0]
        if "?" in myUrl:
            myUrl = myUrl.split("?")[0]
        if "@" in myUrl:
            total = myUrl.count("@")
            if total > 1:
                myUrl = myUrl.split("@")
                screen_names = [u.strip() for u in myUrl]
                print(screen_names)
            else:
                myUrl = myUrl.split("@")[-1]
                screen_names = [myUrl.strip()]
        # Buscar el documento por el screenName en MongoDB
        # documento = collection.find_one({"screenName": screen_name})
        for screen_name in screen_names:
            documento = collection.find_one({"screenName": {'$regex': f'^{screen_name}$', "$options": 'i'}})

            # Verificar si se encontró un documento
            if documento:
                # Hacer una copia del documento sin el campo _id
                copia = documento.copy()
                itemId = documento.get('_id')
                copia.pop('_id', None)

                # Realizar las modificaciones en el documento
                copia["contextA"] = myCapitalize(row["Contexto del Medio"])
                tipo_medio = row["Tipo del Medio"]
                copia["typeA"] = myCapitalize(tipo_medio)
                copia["country"] = myCapitalize(row["PAÍS"])
                copia["region"] = myCapitalize(row["REGIÓN"])
                copia["prov"] = myCapitalize(row["PROVINCIA"])
                copia["city"] = myCapitalize(row["CIUDAD"])
                copia["parish"] = myCapitalize(row["PARROQUIA"])

                # Actualizar el documento en MongoDB
                filter = {"_id": itemId}
                collection.update_one(filter, {"$set": copia})
            else:
                # Mostrar mensaje de columna "Twitter" vacía
                print(f"No se encontró el documento para el username: [{fullUrl}] [{screen_name}]")

# Cerrar la conexión a MongoDB
client.close()
