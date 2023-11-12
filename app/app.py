from flask import Flask, render_template
import pandas as pd
import json
import folium
import os
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def load_data_from_json(json_file="app/data/wifi_data.json"):
    json_file_path = os.path.abspath(json_file)
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data

def analyze_and_visualize(data):
    df = pd.DataFrame(data)

    # Analyze and visualize data (add your analysis code here)
    # For example, let's create a bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='etat2', y='nombre_de_borne_wifi', data=df)
    plt.title('Nombre de bornes WiFi par état')
    plt.xlabel('État')
    plt.ylabel('Nombre de bornes WiFi')

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Encode the image to base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    # Return the encoded image
    return f"data:image/png;base64,{encoded_image}"

@app.route('/')
def index():
    # Load data
    data = load_data_from_json("app/data/wifi_data.json")

    # Analyze and visualize data
    chart_image = analyze_and_visualize(data)

    # Create a map with Folium
    wifi_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles='OpenStreetMap')
    for index, row in pd.DataFrame(data).iterrows():
        folium.Marker(location=[row['geo_point_2d']['lat'], row['geo_point_2d']['lon']],
                      popup=row['nom_site']).add_to(wifi_map)

    # Save the map
    wifi_map.save('app/static/wifi_map.html')

    # Render the HTML template with the map and chart
    return render_template('index.html', wifi_map_url='wifi_map.html', chart_image=chart_image)

if __name__ == '__main__':
    Flask.run(app, port=8000, host="0.0.0.0", debug=True)
