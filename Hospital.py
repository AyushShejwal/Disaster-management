import requests
import folium

api_key = 'OtI61YLZhSo6iOYEnbiJfCVr3DIyZjCO'  # Replace with your TomTom API key
lat, lon = 37.7749, -122.4194  # Example: Latitude and Longitude for San Francisco
radius = 500000  # Search radius in meters
category = 'hospital'  # Category of POI

# Construct the Search API URL
url = f'https://api.tomtom.com/search/2/poiSearch/{category}.json?lat={lat}&lon={lon}&radius={radius}&key={api_key}'

# Make the GET request
response = requests.get(url)

# Initialize a map centered at the requested location
map = folium.Map(location=[lat, lon], zoom_start=13)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON data
    hospitals_info = response.json()
    # Iterate through the results and add markers to the map
    for result in hospitals_info.get('results', []):
        hospital_name = result.get('poi', {}).get('name')
        hospital_address = result.get('address', {}).get('freeformAddress')
        hospital_lat = result.get('position', {}).get('lat')
        hospital_lon = result.get('position', {}).get('lon')
        
        # Add marker to the map
        folium.Marker([hospital_lat, hospital_lon], popup=f"{hospital_name}, {hospital_address}").add_to(map)
        
        print(f'Name: {hospital_name}, Address: {hospital_address}')
else:
    print(f'Failed to retrieve data: {response.status_code}')

# Save the map to an HTML file
map.save('nearby_hospitals_map.html')
