import requests
import pymongo

# Configuration MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "hotelDB"
COLLECTION_NAME = "hotelDB"

# Configuration Amadeus API
AMADEUS_API_URL = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
ACCESS_TOKEN = "IhuuzBHyzxXBwXIfmvvmerLO5vCA"  # Remplacez par votre token dynamique
CITY_CODE = "PAR"  # Code IATA de la ville (ex: PAR pour Paris)

# Connexion à MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_hotels():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "cityCode": CITY_CODE
    }
    response = requests.get(AMADEUS_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erreur: {response.status_code}, {response.text}")
        return []

def save_to_mongodb(hotels):
    if hotels:
        collection.insert_many(hotels)
        print(f"{len(hotels)} hôtels enregistrés dans MongoDB.")
    else:
        print("Aucun hôtel à enregistrer.")

if __name__ == "__main__":
    hotels = fetch_hotels()
    save_to_mongodb(hotels)