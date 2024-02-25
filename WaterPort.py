#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 03:03:31 2024

@author: abc
"""

import requests
import folium

api_key = 'OtI61YLZhSo6iOYEnbiJfCVr3DIyZjCO'  # Replace with your TomTom API key
lat, lon = 37.7749, -122.4194  # Latitude and Longitude for San Francisco
radius = 100000  # Search radius in meters, adjusted to 100km for this example
search_term = 'water port'  # Change the search term to "water port"

# Construct the Search API URL for keyword search
url = f"https://api.tomtom.com/search/2/poiSearch/{search_term}.json?lat={lat}&lon={lon}&radius={radius}&key={api_key}"

# Make the GET request
response = requests.get(url)

# Initialize a map centered at the requested location
map = folium.Map(location=[lat, lon], zoom_start=10)  # Adjust zoom level as needed

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON data
    poi_info = response.json()
    # Iterate through the results and add markers to the map
    for result in poi_info.get('results', []):
        poi_name = result.get('poi', {}).get('name')
        poi_address = result.get('address', {}).get('freeformAddress')
        poi_lat = result.get('position', {}).get('lat')
        poi_lon = result.get('position', {}).get('lon')
        
        # Add marker to the map for each water port found
        folium.Marker([poi_lat, poi_lon], popup=f"{poi_name}, {poi_address}").add_to(map)
        
        print(f'Name: {poi_name}, Address: {poi_address}')
else:
    print(f"Failed to retrieve data: {response.status_code}")

# Save the map to an HTML file
map.save('nearby_water_ports_map.html')


