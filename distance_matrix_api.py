import requests
import logging

def get_distance_matrix(API_KEY, origin, destination, unit, travel_mode, timestamp):
    modes = ['driving', 'bicycling', 'walking', 'transit'] if travel_mode == 'fastest' else [travel_mode]

    results = []

    for mode in modes:
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json'
        params = {
            'units': unit,
            'origins': origin,
            'destinations': destination,
            'mode': mode,
            'key': API_KEY,
            'departure_time': timestamp
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Check if the response has the needed data
                if 'rows' in data and data['rows']:
                    elements = data['rows'][0]['elements'][0]
                    if 'duration' in elements and 'distance' in elements:
                        results.append({
                            'duration': elements['duration']['text'],
                            'distance': elements['distance']['text'],
                            'mode': mode
                        })
            else:
                logging.error(f"Google Maps API request failed with status {response.status_code}")
        except requests.RequestException as e:
            logging.exception(f"Request to Google Maps API failed: {e}")

    return results