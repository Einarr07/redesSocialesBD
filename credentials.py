from os import getenv

from dotenv import load_dotenv
load_dotenv(".env-prod")
mongoCredentials = {
    "host": getenv("MONGO_HOST"),
    "port": int(getenv("MONGO_PORT")),
    "username": getenv("MONGO_USERNAME"),
    "password": getenv("MONGO_PASSWORD"),
    "authSource": getenv("MONGO_AUTH_SOURCE"),
    "authMechanism": getenv("MONGO_AUTH_MECHANISM"),
}
print(f"Mongo credentials [{mongoCredentials}]")
