import pandas as pd
import requests
import time
import os, sys
import json
from functools import wraps


# Set your Google Maps API key (uncomment this if you wish to access your key from a text file)
# with open('your_secret_api_key.txt') as f:
#     API_KEY = f.read().strip()

# Set up caching
CACHE_FILE = 'cache.json'

if os.path.isfile(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)
else:
    cache = {}

def cached(func):
    """Decorator function to cache API responses."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        else:
            result = func(*args, **kwargs)
            cache[key] = result
            with open(CACHE_FILE, 'w') as f:
                json.dump(cache, f)
            return result
    return wrapper


# Load data from Excel file
data = pd.read_excel('input.xlsx')

# Create empty lists to hold the results
distances = []
durations = []


def main():
# Loop through each row in the input data
    for i, row in data.iterrows():
        origin = row['origin']
        destination = row['destination']
        
        @cached
        def get_distance_matrix(origin, destination, unit, mode):
            """Function to send the Distance Matrix API request and parse the response."""
            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units={unit}&origins={origin}&destinations={destination}&mode={mode}&key={API_KEY}'
            response = requests.get(url)
            dt = response.json()
            if 'rows' in dt and len(dt['rows']) > 0 and 'elements' in dt['rows'][0] and len(dt['rows'][0]['elements']) > 0:
                if 'distance' in dt['rows'][0]['elements'][0]:
                    duration = dt['rows'][0]['elements'][0]['duration']['text']
                    distance = dt['rows'][0]['elements'][0]['distance']['text']
                    return distance, duration
                else:
                    return "Error: No route found", "Error: No route found"
            else:
                return "Error: Invalid response format", "Error: Invalid response format"

        # Get the distance matrix for this row's origin and destination
        distance, duration = get_distance_matrix(origin, destination, unit, mode)

        # Append the results to the respective lists
        distances.append(distance)
        durations.append(duration)

        #time.sleep(0.1)

    # Add the new columns to the input data
    data['distance'] = distances
    data['duration'] = durations

    # Save the updated data to an Excel file
    data.to_excel('output.xlsx', index=False)
    print('See the output.xlsx file')






if __name__ == '__main__':
    print("""\nThis script is designed to auto calculate distance and time between origin-destination pairs in a spreadsheet.\n
          IMPORTANT: Make sure you place next to this executable, your 'input.xlsx' file containing two columns: origin and destination,
          and that it has only one sheet.\n
          The next prompt will ask you for the different parameters. THANK YOU !
          """)
    API_KEY = str(input("\tPlease paste your google maps api key here: ")).strip()
    unit = str(input("\tPlease provide the desired unit (km/mi), type: metric or imperial:   "))
    mode = str(input("\tPlease provide the transportation mode: driving, bicycling, walking, transit:   "))
    #unit = sys.argv[1]
    main()