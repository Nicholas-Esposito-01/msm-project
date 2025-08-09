import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

MONGO_USER = os.getenv('MONGO_USER', 'root')
MONGO_PASS = os.getenv('MONGO_PASS', 'example')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_DB = os.getenv('MONGO_DB', 'my_database')

client: Optional[AsyncIOMotorClient] = None

def get_mongo_uri() -> str:
    # authSource=admin è importante quando si usa l'utente root
    return f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"

async def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        uri = get_mongo_uri()
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        # Forza una selezione del server per verificare la connessione
        await client.server_info()
    return client


def get_database():
    # Non asincrono: ritorna l'oggetto Database collegato al client
    global client
    if client is None:
        # se non inizializzato sincrono, inizializza un client sincrono minimo
        client_local = AsyncIOMotorClient(get_mongo_uri())
        return client_local[MONGO_DB]
    return client[MONGO_DB]