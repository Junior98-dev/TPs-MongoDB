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
    
# Fonction pour stocker les films dans MongoDB
def store_movies(movies):
    for movie in movies:
        movie_details = {
            "Titre": movie.get('Title'),
            "Année": movie.get('Year'),
            "ID_IMDb": movie.get('imdbID'),
            "Genre": None,  # Récupération détaillée plus tard
            "Réalisateur": None,
            "Acteurs": None,
            "Synopsis": None
        }

        # Récupérer des détails supplémentaires sur chaque film
        details_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie['imdbID']}"
        details_response = requests.get(details_url)
        if details_response.status_code == 200:
            details_data = details_response.json()
            movie_details["Genre"] = details_data.get('Genre')
            movie_details["Réalisateur"] = details_data.get('Director')
            movie_details["Acteurs"] = details_data.get('Actors')
            movie_details["Synopsis"] = details_data.get('Plot')

        # Vérification avant insertion pour éviter les doublons
        if not collection.find_one({"ID_IMDb": movie_details['ID_IMDb']}):
            collection.insert_one(movie_details)
            print(f"Film ajouté : {movie_details['Titre']}")
        else:
            print(f"Film déjà existant : {movie_details['Titre']}")

# Fonction pour lister tous les films dans la base de données
def list_all_movies():
    movies = collection.find()
    for movie in movies:
        print(f"Titre: {movie['Titre']}, Année: {movie['Année']}, ID_IMDb: {movie['ID_IMDb']}")


# Fonction pour afficher les détails d'un film spécifique
def show_movie_details(imdb_id):
    movie = collection.find_one({"ID_IMDb": imdb_id})
    if movie:
        print("Détails du film :")
        for key, value in movie.items():
            if key != "_id":
                print(f"{key}: {value}")
    else:
        print("Aucun film trouvé avec cet ID IMDb.")