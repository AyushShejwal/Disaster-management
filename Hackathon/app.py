import requests
from datetime import date
from datetime import timedelta
from geopy.distance import geodesic
from flask import Flask, jsonify, render_template
import folium
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


def create_folium_map():
    map = folium.Map(location=[37.7749, -122.4194], zoom_start=8)
    # Define the bounds for the entire state of California
    max_bounds = [[32.5, -124.5], [42, -114]]
    map.fit_bounds(max_bounds)

    # Restrict the user from dragging the map outside the specified bounds
    # Optional: Add a popup for LatLng information
    map.add_child(folium.LatLngPopup())

    return map


@app.route('/earthquake_data')
def earthquake_data():
    map = create_folium_map()

    today = date.today()
    yesterday = today - timedelta(days=1)

    # Define the center (San Francisco) latitude and longitude
    latitude = 37.7749
    longitude = -122.4194
    radius = 100  # Radius in kilometers

    # Construct the API URL for earthquakes within 50km of San Francisco's center
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-01-01&endtime=2023-01-02&minmagnitude=1.0&latitude={latitude}&longitude={longitude}&maxradiuskm={radius}"

    # Make the request
    response = requests.get(url)

    if response.status_code == 200:
        # Convert the response to JSON format
        earthquakes_data = response.json()

        # Process or print the data
        for earthquake in earthquakes_data['features']:
            # Get the location from the earthquake data
            quake_location = earthquake['geometry']['coordinates'][1], earthquake['geometry']['coordinates'][0]
            # Get the magnitude and place for the popup
            magnitude = earthquake['properties']['mag']
            place = earthquake['properties']['place']
            # Create a marker for each earthquake
            folium.Marker(
                location=quake_location,
                popup=f"Magnitude: {magnitude}\nLocation: {place}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(map)

        # Convert Folium map object to HTML content
        html_content = map._repr_html_()
        return html_content
    else:
        return jsonify({"error": f"Error fetching earthquake data: {response.status_code}"})


@app.route('/food_bank_data')
def food_bank_data():
    map = create_folium_map()

    api_key = 'OtI61YLZhSo6iOYEnbiJfCVr3DIyZjCO'
    lat, lon = 37.7749, -122.4194
    radius = 50000
    search_term = 'food bank'

    url = f"https://api.tomtom.com/search/2/poiSearch/{search_term}.json?lat={lat}&lon={lon}&radius={radius}&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        poi_info = response.json()
        for result in poi_info.get('results', []):
            poi_name = result.get('poi', {}).get('name')
            poi_address = result.get('address', {}).get('freeformAddress')
            poi_lat = result.get('position', {}).get('lat')
            poi_lon = result.get('position', {}).get('lon')

            folium.Marker([poi_lat, poi_lon],
                          popup=f"{poi_name}, {poi_address}").add_to(map)

        html_content = map._repr_html_()
        return html_content
    else:
        return jsonify({"error": f"Error fetching food bank data: {response.status_code}"})


@app.route('/healthcare_data')
def healthcare_data():
    map = create_folium_map()

    api_key = 'a655989a51dc495d9a58880f3dc27dfd'
    lat, lon = 37.7749, -122.4194
    radius = 5000

    url = f'https://api.geoapify.com/v2/places?categories=healthcare.hospital&filter=circle:{lon},{lat},{radius}&apiKey={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        healthcare_data = response.json()

        for place in healthcare_data['features']:
            name = place['properties'].get('name', 'No name provided')
            address = f"{place['properties'].get('address_line1', 'No address provided')}, {place['properties'].get('city', 'No city provided')}"
            place_lat = place['geometry']['coordinates'][1]
            place_lon = place['geometry']['coordinates'][0]

            folium.Marker(
                [place_lat, place_lon],
                popup=f"{name}, {address}"
            ).add_to(map)

        html_content = map._repr_html_()
        return html_content
    else:
        return jsonify({"error": f"Error fetching healthcare data: {response.status_code}"})


@app.route('/natural_disaster_data')
def natural_disaster_data():
    map = create_folium_map()

    sf_coords = (37.7749, -122.4194)
    radius_km = 500
    url = "https://eonet.gsfc.nasa.gov/api/v2.1/events"

    response = requests.get(url)

    def get_marker_color(category_title):
        if "Earthquakes" in category_title:
            return 'red'
        elif "Wildfires" in category_title:
            return 'orange'
        elif "Severe Storms" in category_title:
            return 'blue'
        else:
            return 'green'

    def is_near_sf(event_coords):
        distance = geodesic(sf_coords, event_coords).kilometers
        return distance <= radius_km

    if response.status_code == 200:
        data = response.json()

        for event in data['events']:
            category_title = event['categories'][0]['title']
            marker_color = get_marker_color(category_title)
            for geometry in event['geometries']:
                if geometry['type'] == 'Point':
                    coords = (geometry['coordinates'][1],
                              geometry['coordinates'][0])
                    if is_near_sf(coords):
                        folium.Marker(
                            location=[coords[0], coords[1]],
                            popup=f"{event['title']}<br><a href='{event['link']}' target='_blank'>More info</a>",
                            icon=folium.Icon(color=marker_color)
                        ).add_to(map)

        html_content = map._repr_html_()
        return html_content
    else:
        return jsonify({"error": f"Error fetching natural disaster data: {response.status_code}"})


@app.route('/roadclosure_data')
def roadclosure_data():
    map = create_folium_map()

    api_key = 'OtI61YLZhSo6iOYEnbiJfCVr3DIyZjCO'
    bbox = '-122.45,37.77,-122.37,37.81'
    url = f'https://api.tomtom.com/traffic/services/5/incidentDetails?key={api_key}&bbox={bbox}&language=en-GB&detail=full&format=json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for incident in data['incidents']:
            coords = incident['geometry']['coordinates']
            coords = [(lat, lon) for lon, lat in coords]
            folium.PolyLine(locations=coords, color='red').add_to(map)

        html_content = map._repr_html_()
        return html_content
    else:
        return jsonify({"error": f"Error fetching traffic data: {response.status_code}"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
