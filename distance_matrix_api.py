import requests
from caching import cached


# Set your Google Maps API key (uncomment this if you wish to access your key from a text file)
# with open('your_secret_api_key.txt') as f:
#     API_KEY = f.read().strip()

@cached
def get_distance_matrix(API_KEY, origin, destination, unit):
    """Function to send the Distance Matrix API request and parse the response for each travel mode"""

    modes = ['driving', 'bicycling', 'walking', 'transit']
    distance_and_duration_per_mode = []

    for mode in modes:
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units={unit}&origins={origin}&destinations={destination}&mode={mode}&key={API_KEY}'
        response = requests.get(url)
        dt = response.json()

        if 'rows' in dt and len(dt['rows']) > 0 and 'elements' in dt['rows'][0] and len(dt['rows'][0]['elements']) > 0:
            if 'distance' in dt['rows'][0]['elements'][0]:
                duration = dt['rows'][0]['elements'][0]['duration']['text']
                distance = dt['rows'][0]['elements'][0]['distance']['text']
                distance_and_duration_per_mode.append((duration, distance, mode))

    return distance_and_duration_per_mode     
        



    





