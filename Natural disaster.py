import requests
from geopy.distance import geodesic
import folium

# Initialize Folium map centered around San Francisco
map = folium.Map(location=[37.7749, -122.4194], zoom_start=6)

# San Francisco coordinates
sf_coords = (37.7749, -122.4194)
radius_km = 500

# EONET API URL
url = "https://eonet.gsfc.nasa.gov/api/v2.1/events"

# Make the GET request
response = requests.get(url)

def get_marker_color(category_title):
    """Return a color based on the event's category."""
    if "Earthquakes" in category_title:
        return 'red'
    elif "Wildfires" in category_title:
        return 'orange'
    elif "Severe Storms" in category_title:
        return 'blue'
    else:
        return 'green'  # Default color for other types of events

def is_near_sf(event_coords):
    """Check if the event is within the specified radius from San Francisco."""
    distance = geodesic(sf_coords, event_coords).kilometers
    return distance <= radius_km

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Filter and add markers for events near San Francisco
    for event in data['events']:
        category_title = event['categories'][0]['title']  # Assuming the first category is the primary one
        marker_color = get_marker_color(category_title)  # Get marker color based on the event category
        for geometry in event['geometries']:
            # Some events have multiple coordinates; we check each one
            if geometry['type'] == 'Point':
                coords = (geometry['coordinates'][1], geometry['coordinates'][0])  # Flip coords to (lat, lon)
                if is_near_sf(coords):
                    # Add a customized marker to the map
                    folium.Marker(
                        location=[coords[0], coords[1]],
                        popup=f"{event['title']}<br><a href='{event['link']}' target='_blank'>More info</a>",
                        icon=folium.Icon(color=marker_color)  # Use the determined color
                    ).add_to(map)
                    print(f"Event: {event['title']}")
                    print(f"Date: {geometry['date']}")
                    print(f"Coordinates: {coords}")
                    print(f"Link: {event['link']}")
                    print("-----")
else:
    print(f"Failed to retrieve data: {response.status_code}")

# Save the map to an HTML file
map.save('eonet_events_near_sf.html')
