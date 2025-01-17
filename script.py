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

# Fonction pour rechercher des films via l'API OMDb
keyword = input("Entrez le titre de votre film : ")
def search_movies(keyword):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('Search'):
            return data['Search']
        else:
            print("Aucun film trouvé.")
            return []
    else:
        print("Erreur lors de la requête API OMDb.")
        return []

search_movies({keyword})