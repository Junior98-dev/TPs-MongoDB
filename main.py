import os
import requests
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from loguru import logger



#onfiguration 
AMADEUS_API_KEY= 'b4Yd0QrFGeZZCzkR9PdaT0b0SFObT0er'
AMADEUS_SECRET_KEY='fJ4hGQnmuSMMhdwA'
MONGO_URI='mongodb://localhost:27017'
MONGO_DB='hotelDB'

# Configuration MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
hotels_collection = db["hotelDB"]



# FastAPI
app = FastAPI()

logger.add("app.log", level="INFO", rotation="10MB")

# Configuration API Amadeus
AMADEUS_API_KEY = "b4Yd0QrFGeZZCzkR9PdaT0b0SFObT0er"
AMADEUS_SECRET_KEY = "fJ4hGQnmuSMMhdwA"
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
HOTEL_SEARCH_URL = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"

# Obtenir un token d'authentification
def get_access_token():
    
    data = {

        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_SECRET_KEY,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise HTTPException(status_code=401, detail="Échec de l'authentification avec Amadeus")
    
logger.info("Connexion à l'API Amadeus et MongoDB réussie.")

# Endpoint pour récupérer les hôtels et les stocker
@app.get("/hotels/{city_code}")
def get_hotels(city_code: str):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"cityCode": city_code}
    response = requests.get(HOTEL_SEARCH_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur API Amadeus")

    hotels_data = response.json().get("data", [])
    
    # Sauvegarde dans MongoDB
    hotels = []
    for hotel in hotels_data:
        hotel_entry = {
            "hotelId": hotel.get("hotelId"),
            "name": hotel.get("name"),
            "city": city_code,
            "address": hotel.get("address", {}).get("lines", [""])[0],
        }
        hotels_collection.update_one({"hotelId": hotel_entry["hotelId"]}, {"$set": hotel_entry}, upsert=True)
        hotels.append(hotel_entry)
    logger.info(f"nouveaux hôtels : {hotels}")

    return {"hotels": hotels}

# Endpoint pour récupérer les hôtels sauvegardés
@app.get("/hotels/saved/{city}")
def get_saved_hotels(city: str):
    hotels = list(hotels_collection.find({"city": city}, {"_id": 0}))
    return {"hotels": hotels}
