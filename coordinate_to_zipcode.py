import requests

def get_zip_code(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}'
    response = requests.get(url)
    print("API Response:", response.text)  # Add this line to check the response
    data = response.json()
    if 'address' in data:
        return data['address'].get('postcode', None)
    return None

# Example coordinates (San Francisco)
latitude = 37.7749
longitude = -122.4194

zip_code = get_zip_code(latitude, longitude)
print("Zip Code:", zip_code)
