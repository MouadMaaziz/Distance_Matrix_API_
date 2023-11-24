import os, sys
from datetime import datetime
import pandas as pd
from .distance_matrix_api import get_distance_matrix
from parse_duration import duration_to_delta



if __name__ == '__main__':


    print("""\nThis script is designed to auto calculate distance and time between origin-destination pairs in a spreadsheet.\n
          IMPORTANT: Make sure you place next to this executable, your 'input.xlsx' file containing two columns: origin and destination,
          and that it has only one sheet.\n
          The next prompt will ask you for the different parameters. THANK YOU !
          """)
    API_KEY = str(input("\tPlease paste your google maps api key here: ")).strip()
    unit = str(input("\tPlease provide the desired unit (km/mi), type: metric or imperial:   "))
    mode = str(input("\tPlease provide the transportation mode: driving, bicycling, walking, transit:   "))



    # Load data from Excel file
    data = pd.read_excel('input.xlsx')

    # Create empty lists to hold the results
    distances = []
    durations = []
    for i, row in data.iterrows():
        origin = row['origin']
        destination = row['destination']

    # Get the distance matrix for this row's origin and destination
    distance, duration = get_distance_matrix(API_KEY, origin, destination, unit, mode)
    # Append the results to the respective lists
    distances.append(distance)
    durations.append(duration)

    # Add the new columns to the input data
    data['distance'] = distances
    data['duration'] = durations
    data['departure_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['arriving_time'] = datetime.now() + duration_to_delta(data['duration'])

    output_file = 'output.xlsx'
    # if output.xlsx exists:
    # store data in a new output

    try:
        existing_df = pd.read_excel(output_file)
        updated_df = existing_df.append(data, ignore_index=True)
        updated_df.to_excel(output_file, index=False)
    except FileNotFoundError:
        print('Creating outpu.xlsx')
        data.to_excel(output_file, index=False)

    
    print('See the output.xlsx file')




 