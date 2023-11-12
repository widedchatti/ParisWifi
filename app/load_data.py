from pymongo import MongoClient
from bson import json_util
import json

def load_data_from_mongo():
    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["paris_wifi_database"]
    wifi_collection = db["wifi_data"]

    # Charger les données depuis MongoDB
    cursor = wifi_collection.find({})
    wifi_data = list(cursor)

    return wifi_data

def save_data_to_json(data, output_file="wifi_data.json"):
    # Convertir les ObjectId en chaînes de caractères
    for entry in data:
        entry["_id"] = str(entry["_id"])

    # Sauvegarder les données au format JSON
    with open(output_file, "w") as file:
        json.dump(data, file, default=json_util.default, indent=2)

if __name__ == "__main__":
    # Charger les données depuis MongoDB
    data = load_data_from_mongo()

    # Sauvegarder les données au format JSON
    save_data_to_json(data)

    print("Données chargées depuis MongoDB et sauvegardées dans wifi_data.json.")
