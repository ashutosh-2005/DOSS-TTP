import requests
from geopy.distance import geodesic
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Function to get latitude and longitude using Nominatim API
def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    response = requests.get(url).json()
    if response:
        return (float(response[0]['lat']), float(response[0]['lon']))
    else:
        return None

# Function to find nearby places within a radius
def find_nearby_places(lat, lon, radius_km, place_type):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node(around:{radius_km*1000},{lat},{lon})["{place_type}"];
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    places = []
    for element in data['elements']:
        place_lat = element['lat']
        place_lon = element['lon']
        place_name = element.get('tags', {}).get('name', 'Unnamed Place')
        place_distance = geodesic((lat, lon), (place_lat, place_lon)).km
        if place_distance <= radius_km:
            places.append({
                'name': place_name,
                'latitude': place_lat,
                'longitude': place_lon,
                'distance_km': round(place_distance, 2)
            })
    return places

# Example Usage
if __name__ == "__main__":
    address = "Central Park, New York"
    radius_km = 2  # Radius in kilometers
    place_type = "restaurant"  # Specify the type of place

    coords = get_coordinates(address)
    if coords:
        lat, lon = coords
        nearby_places = find_nearby_places(lat, lon, radius_km, place_type)
        print(f"Places within {radius_km} km of {address}:")
        for place in nearby_places:
            print(f"- {place['name']} ({place['distance_km']} km away)")
    else:
        print("Address not found.")
