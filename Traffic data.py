import requests
import folium
# Replace 'YOUR_TOMTOM_API_KEY' with your actual TomTom API key
api_key = 'OtI61YLZhSo6iOYEnbiJfCVr3DIyZjCO'
map_center = [37.7749, -122.4194]  # Example center: San Francisco
m = folium.Map(location=map_center, zoom_start=13)

# Define the bounding box for the area you're interested in
# Format: "longitudeSW,latitudeSW:longitudeNE,latitudeNE"
# Example coordinates define a box around a central point in San Francisco
bbox = '-122.45,37.77,-122.37,37.81'

# TomTom Traffic API endpoint with parameters
url = f'https://api.tomtom.com/traffic/services/5/incidentDetails?key={api_key}&bbox={bbox}&language=en-GB&detail=full&format=json'

# Make the GET request to the TomTom Traffic API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the response JSON data
    data = response.json()
else:
    print('Failed to retrieve data:', response.status_code)




for incident in data['incidents']:
    # Extract coordinates for the line string
    coords = incident['geometry']['coordinates']
    # Folium requires coordinates in (lat, lon) format, but GeoJSON is (lon, lat)
    coords = [(lat, lon) for lon, lat in coords]
    # Create a line with the coordinates
    folium.PolyLine(locations=coords, color='red').add_to(m)

# Save the map to an HTML file
m.save('traffic_incidents_map.html')


#convert to html/css/javascript