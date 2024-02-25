import requests
import folium

api_key = 'a655989a51dc495d9a58880f3dc27dfd'  # Your Geoapify API key
lat, lon = 37.7749, -122.4194  # Latitude and Longitude for San Francisco
radius = 10000  # Search radius in meters

# Construct the API URL for searching hospitals
url = f'https://api.geoapify.com/v2/places?categories=healthcare.hospital&filter=circle:{lon},{lat},{radius}&apiKey={api_key}'

# Make the GET request
response = requests.get(url)

# Initialize a map centered at the requested location
map = folium.Map(location=[lat, lon], zoom_start=13)

if response.status_code == 200:
    # Parse the response JSON data
    healthcare_data = response.json()
    
    # Iterate through the results and add markers to the map
    for place in healthcare_data['features']:
        # Some places might not have a 'name' property, handling such cases
        name = place['properties'].get('name', 'No name provided')
        address = f"{place['properties'].get('address_line1', 'No address provided')}, {place['properties'].get('city', 'No city provided')}"
        place_lat = place['geometry']['coordinates'][1]
        place_lon = place['geometry']['coordinates'][0]
        
        # Add marker to the map
        folium.Marker(
            [place_lat, place_lon],
            popup=f"{name}, {address}"
        ).add_to(map)
else:
    print(f"Failed to retrieve data: {response.status_code}")

# Save the map to an HTML file
map.save('nearby_healthcare_map.html')
