import requests
import pymongo
from pymongo import MongoClient

# Configuration
OMDB_API_KEY = 'f5c61273'  # Remplacez par votre clé API OMDb
MONGO_URI = 'mongodb://localhost:27017/'  # URL de connexion MongoDB
DATABASE_NAME = 'movie_database'
COLLECTION_NAME = 'movies'

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


