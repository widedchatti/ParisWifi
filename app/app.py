import requests
from pymongo import MongoClient
import time
from flask import Flask, render_template
import pandas as pd
import folium
import json
import os

url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/sites-disposant-du-service-paris-wi-fi/records?limit=100"

# Fonction pour faire la requête à l'API
def request(offsetIndex):
    try:
        response = requests.get(url + f'&offset={offsetIndex}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error = {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Request Error : {e}')

# Fonction pour télécharger les données dans MongoDB
def download_database():
    #client = MongoClient("mongodb://localhost:27017/")
    client = MongoClient("mongodb://root:root@my-mongodb:27017/")
    db = client["paris_wifi_database"]
    wifi_collection = db["wifi_data"]

    data = request(0)
    totalResults = 277

    for i in range(0, totalResults, 100):
        data = request(i)
        if data:
            data_per_request = data['results']
            wifi_collection.insert_many(data_per_request)
            print(f"Chunk starting at index {i} downloaded successfully!")
            time.sleep(6)

# Fonction pour charger les données depuis MongoDB
def load_data_from_mongo():
    #client = MongoClient("mongodb://localhost:27017/")
    client = MongoClient("mongodb://root:root@my-mongodb:27017/")

    db = client["paris_wifi_database"]
    wifi_collection = db["wifi_data"]

    cursor = wifi_collection.find({})
    wifi_data = list(cursor)

    return wifi_data

# Fonction pour sauvegarder les données au format JSON
def save_data_to_json(data, output_file="app/data/wifi_data.json"):
    for entry in data:
        entry["_id"] = str(entry["_id"])

    with open(output_file, "w") as file:
        json.dump(data, file, indent=2)




# Fonction pour charger les données depuis un fichier JSON
def load_data_from_json(json_file="app/data/wifi_data.json"):
    json_file_path = os.path.abspath(json_file)
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data


# Fonction principale Flask
app = Flask(__name__)

@app.route('/')
def index():
    # Charger les données depuis MongoDB
    data = load_data_from_mongo()

    # Sauvegarder les données au format JSON
    save_data_to_json(data)

    # Charger les données depuis le fichier JSON
    data_from_json = load_data_from_json("app/data/wifi_data.json")

    # Créer une carte avec Folium
    wifi_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles='OpenStreetMap')
    for index, row in pd.DataFrame(data_from_json).iterrows():
        folium.Marker(location=[row['geo_point_2d']['lat'], row['geo_point_2d']['lon']],
                      popup=row['nom_site']).add_to(wifi_map)

    # Sauvegarder la carte
    wifi_map.save('app/static/wifi_map.html')

    # Rendre le modèle HTML avec la carte
    return render_template('index.html', wifi_map_url='wifi_map.html')


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)
