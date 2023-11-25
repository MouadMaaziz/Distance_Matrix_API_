import os, sys
from datetime import datetime
import glob
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
    # data = pd.read_excel(glob.glob("output*.xlsx")[0])

    # Create empty lists to hold the results
    distances = []
    durations = []
    modes = []
    
    for i, row in data.iterrows():
        origin = row['origin']
        destination = row['destination']

        # Get the distance matrix for this row's origin and destination and sort them by duration.
        distance_and_duration_per_mode = get_distance_matrix(API_KEY, origin, destination, unit)
        fastest_navigation = sorted(distance_and_duration_per_mode,
                                    key= lambda x:duration_to_delta(x[0]).total_seconds()
                            )
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


    # Get the last created output excel as the base file to append to
    old_output_file = sorted(glob.glob("output*.xlsx"), key= lambda x:os.path.getctime(x), reverse= True)[0]

    # Create a new output file with ctime in its name
    new_output_file = f'output_{datetime.now().strftime("%Y-%m-%d_at_%H_%M_%S")}.xlsx'



    # if output.xlsx exists append if not create a new one:
    try:
        existing_df = pd.read_excel(old_output_file)
        updated_df = pd.concat([existing_df, data], ignore_index=True)
        updated_df.to_excel(new_output_file, index=False)
        for excel in glob.glob("output*.xlsx"):
            if excel != new_output_file:
                os.remove(excel)
        print(f'Created {new_output_file}')

    except FileNotFoundError:
        print('Creating output.xlsx')
        data.to_excel(new_output_file, index=False)
        os.remove(old_output_file)
    print(f'Created {new_output_file}')




 