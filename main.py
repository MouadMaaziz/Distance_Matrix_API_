import os, sys
from datetime import datetime
import pandas as pd
from distance_matrix_api import get_distance_matrix
from parse_duration import duration_to_delta



if __name__ == '__main__':

    print("""\nThis script is designed to auto calculate distance and time between origin-destination pairs in a spreadsheet.\n
          IMPORTANT: Make sure you place next to this executable, your 'input.xlsx' file containing two columns: origin and destination,
          and that it has only one sheet.\n
          The next prompt will ask you for the different parameters. THANK YOU !
          """)
    # API_KEY = str(input("\tPlease paste your google maps api key here: ")).strip()
    API_KEY = 'AIzaSyC6Q1B5ZXLOOihBKlP-sSY-uR82DlU7LZQ'
    unit = str(input("\tPlease provide the desired unit (km/mi), type: metric or imperial:   "))

    # Load data from Excel file
    data = pd.read_excel('input.xlsx')

    # Create empty lists to hold the results
    distances = []
    durations = []
    modes = []
    for i, row in data.iterrows():
        origin = row['origin']
        destination = row['destination']

        # Get the distance matrix for this row's origin and destination
        distance_and_duration_per_mode = get_distance_matrix(API_KEY, origin, destination, unit)
        fastest_navigation = sorted(distance_and_duration_per_mode, key= lambda x:duration_to_delta(x[0]).total_seconds())
        duration, distance, mode = fastest_navigation[0]
        # Append the results to the respective lists
        distances.append(distance)
        durations.append(duration)
        modes.append(mode)

    # Add the new columns to the input data
    data['distance'] = distances
    data['duration'] = durations
    data['departure_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['arriving_time'] = datetime.now() + data['duration'].apply(duration_to_delta)
    data['mode'] = modes

    output_file = 'output.xlsx'
    # if output.xlsx exists append if not create a new one:
    try:
        existing_df = pd.read_excel(output_file)
        updated_df = pd.concat([existing_df, data], ignore_index=True)
        updated_df.to_excel(output_file, index=False)
        print('Appended to output.xlsx')

    except FileNotFoundError:
        print('Creating output.xlsx')
        data.to_excel(output_file, index=False)
    
    print('See the output.xlsx file')




 