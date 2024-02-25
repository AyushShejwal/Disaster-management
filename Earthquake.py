
import requests
from datetime import date
from datetime import timedelta
import folium

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
    
    # Initialize a map centered at the requested location
    map = folium.Map(location=[latitude, longitude], zoom_start=10)
    
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
    
    # Save the map to an HTML file
    map.save('earthquakes_map.html')
else:
    print(f"Error fetching data: {response.status_code}")
