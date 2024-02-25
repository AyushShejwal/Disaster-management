import requests

def get_hospitals_in_zip_code(zip_code):
    # Step 1: Convert zip code to latitude and longitude
    nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={zip_code}"
    response = requests.get(nominatim_url)
    data = response.json()
    if not data:
        print(f"No data found for zip code {zip_code}")
        return [], 0  # Return an empty list and 0 for the count if no data is found

    latitude = data[0]['lat']
    longitude = data[0]['lon']

    # Step 2: Query Overpass API for hospitals near the coordinates
    overpass_query = f"""
    [out:json];
    (
        node["amenity"="hospital"](around:1000,{latitude},{longitude});
        way["amenity"="hospital"](around:1000,{latitude},{longitude});
        relation["amenity"="hospital"](around:1000,{latitude},{longitude});
    );
    out body;
    >;
    out skel qt;
    """

    overpass_url = "https://overpass-api.de/api/interpreter"
    response = requests.post(overpass_url, data=overpass_query)
    data = response.json()

    # Step 3: Parse the response and extract hospital details
    hospitals = []
    i = 0
    for element in data['elements']:
        if 'tags' in element and 'name' in element['tags']:
            hospitals.append(element['tags']['name'])
            i += 1  # Increment i only when a hospital is found

    print("Number of hospitals:", i)

    return hospitals, i

# Example usage
zip_code = "94115"  # Example zip code (San Francisco)
hospitals, count = get_hospitals_in_zip_code(zip_code)
print("Hospitals in", zip_code, ":", hospitals)
print("Number of hospitals:", count)
