from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes depuis le frontend

# Connexion à MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/hotelDB"
mongo = PyMongo(app)

@app.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = mongo.db.hotels.find()
    hotel_list = []

    for hotel in hotels:
        hotel_list.append({
            "id": str(hotel["_id"]),
            "nom": hotel["nom"],
            "ville": hotel["ville"],
            "prix": hotel["prix"],
            "image": hotel["image"]
        })

    return jsonify(hotel_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
