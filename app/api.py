#Récupération des données par API!
import requests
import json
from pymongo import MongoClient
import time

url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/sites-disposant-du-service-paris-wi-fi/records?limit=100"
wifi_data = []
offsetIndex = 0

def request(offsetIndex):
    try:
        response = requests.get(url + f'&offset={offsetIndex}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error = {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Request Error : {e}')

def download_database():
    client = MongoClient("mongodb://localhost:27017/")  # Assurez-vous que votre instance MongoDB tourne localement
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

# Appel de la fonction pour télécharger la base de données
download_database()
