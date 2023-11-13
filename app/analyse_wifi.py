#Ce fichier est optionnel j'ai juste essayer avec les biblio python pour faire quelques analyses et visualisations des données et les enregistrer sous format png sous le folder /static
#J'ai aussi crée une carte en utilisant Folium 
# Import des bibliothèques
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import folium
import os

# Fonction pour charger les données depuis un fichier JSON
def load_data_from_json(json_file="app/data/wifi_data.json"):
    with open(json_file, "r") as file:
        data = json.load(file)
    return data

# Fonction pour analyser et visualiser les données WiFi
def analyze_and_visualize(data):
    # Créer un DataFrame à partir des données
    df = pd.DataFrame(data)

    # Créer le dossier 'static' s'il n'existe pas
    static_folder = 'app/static'
    os.makedirs(static_folder, exist_ok=True)

    # Analyser les données et créer des visualisations
    operational_sites = df[df['etat2'] == 'Opérationnel'].shape[0]
    closed_sites = df[df['etat2'] == 'Fermé pour travaux'].shape[0]

    # Afficher les résultats
    print(f"Nombre de sites opérationnels : {operational_sites}")
    print(f"Nombre de sites fermés pour travaux : {closed_sites}")

    # Visualiser les données et sauvegarder l'image
    plt.figure()
    sns.countplot(x='etat2', data=df)
    plt.title('Répartition des états des sites WiFi')
    plt.savefig(os.path.join(static_folder, 'etat_plot.png'))

    # Analyse et visualisation du nombre de bornes WiFi par site
    plt.figure(figsize=(12, 6))
    sns.histplot(df['nombre_de_borne_wifi'], bins=20, kde=True)
    plt.title('Distribution du nombre de bornes WiFi par site')
    plt.xlabel('Nombre de bornes WiFi')
    plt.ylabel('Nombre de sites')
    plt.savefig(os.path.join(static_folder, 'nombre_de_borne_wifi_plot.png'))

    # Analyse et visualisation du nombre de bornes WiFi par arrondissement
    plt.figure(figsize=(14, 8))
    sns.barplot(x='cp', y='nombre_de_borne_wifi', data=df, errorbar=None)
    plt.title('Nombre de bornes WiFi par arrondissement')
    plt.xlabel('Code postal')
    plt.ylabel('Nombre de bornes WiFi')
    plt.savefig(os.path.join(static_folder, 'nombre_de_borne_wifi_arrondissement_plot.png'))

    # Ajout des analyses supplémentaires
    # Analyse de la densité de bornes WiFi par quartier
    df['quartier'] = pd.cut(df['geo_point_2d'].apply(lambda x: x['lat']), bins=4, labels=['Quartier 1', 'Quartier 2', 'Quartier 3', 'Quartier 4'])
    plt.figure(figsize=(14, 8))
    sns.barplot(x='quartier', y='nombre_de_borne_wifi', data=df, errorbar=None)
    plt.title('Densité de bornes WiFi par quartier')
    plt.xlabel('Quartier')
    plt.ylabel('Nombre de bornes WiFi')
    plt.savefig(os.path.join(static_folder, 'densite_bornes_wifi_quartier_plot.png'))

    
    # Créer une carte avec Folium (commentez cette partie si elle provoque des erreurs)
    wifi_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles='OpenStreetMap')

    # Ajouter des marqueurs pour chaque site WiFi
    for index, row in df.iterrows():
        folium.Marker(location=[row['geo_point_2d']['lat'], row['geo_point_2d']['lon']],
                      popup=row['nom_site']).add_to(wifi_map)

    # Afficher la carte
    wifi_map.save(os.path.join(static_folder, 'wifi_map.html'))

if __name__ == "__main__":
    # Charger les données depuis le fichier JSON
    data = load_data_from_json("app/data/wifi_data.json")

    # Analyser et visualiser les données
    analyze_and_visualize(data)
