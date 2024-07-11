import certifi
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

HOST = 'bimodtest.d89cgcx.mongodb.net'
USER = 'root'
PASSWORD = 'V4AXP7dSzeuIaemC'

connection_string = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/?retryWrites=true&w=majority&appName=BimodTest"
client = MongoClient(connection_string, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    col_names = client.get_database('sample_mflix').list_collection_names()
    print(col_names)
except Exception as e:
    print(e)
