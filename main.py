import os, sys
from datetime import datetime
import glob
from datetime import datetime, timedelta
import pandas as pd
from distance_matrix_api import get_distance_matrix
from parse_duration import duration_to_delta
import schedule
import time
import itertools

def scheduled_calculation(API_KEY, unit):

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
    old_output_file = sorted(glob.glob("output*.xlsx"),
                            key= lambda x:os.path.getctime(x),
                            reverse= True)[0]

    # Create a new output file with ctime in its name
    new_output_file = f'output_{datetime.now().strftime("%Y-%m-%d_at_%H_%M_%S")}.xlsx'

    # if output.xlsx exists append if not create a new one:
    try:
        existing_df = pd.read_excel(old_output_file)
        updated_df = pd.concat([existing_df, data], ignore_index=True)
        updated_df.to_excel(new_output_file, index=False)
        for excel in glob.glob("output*.xlsx"):
            if excel != new_output_file:
                try:
                    os.remove(excel)
                except PermissionError:
                    pass

        print(f'Created {new_output_file}')

    except FileNotFoundError:
        print('Creating output.xlsx')
        data.to_excel(new_output_file, index=False)
        os.remove(old_output_file)
        print(f'Created {new_output_file}')

def welcome_message():
    print("""
    Welcome to the Auto Distance and Time Calculator! 

    Get ready to effortlessly calculate distances and travel times between origin-destination pairs in your spreadsheet!

    IMPORTANT: Place this script next to 'input.xlsx,' which should have columns for origin and destination on a single sheet.

    Let's get started! The upcoming prompts will walk you through the setup. Thank you for choosing our tool! 
    """)

def get_user_input():
    API_KEY = str(input("Please paste your Google Maps API key here: ")).strip()
    unit = input("Fantastic! Let's pick the unit of measurement. Enter 'metric' for kilometers or 'imperial' for miles: ")
    return API_KEY, unit

def countdown_display(minutes):
    spinner = itertools.cycle(['—', '\\', '|', '/'])  # Spinner animation characters
    minutes = float(minutes)
    while minutes > 0:  # Convert minutes to float
        print(f"\r Next execution in {round(minutes,2)} minutes  {next(spinner)}          ", end="")
        sys.stdout.flush()
        time.sleep(0.5)  # Adjusted sleep time for faster spinner
        minutes = minutes - (0.5 / 60)  # Decreased minutes by the sleep time
    print("\n", end="")



if __name__ ==  '__main__':
    
    welcome_message()
    
    # User input
    API_KEY, unit = get_user_input()

    # Initial execution
    scheduled_calculation(API_KEY, unit)

    # Schedule the function to run every 1 minute
    schedule.every(1).hours.do(scheduled_calculation, API_KEY, unit)

    # Countdown and execute the function again after 1 minute
    try:
        while True:
            next_run = schedule.idle_seconds()
            time_until_next_run = max(next_run, 0)

            # Convert seconds to hours and minutes for a more user-friendly display
            minutes, remainder = divmod(time_until_next_run, 60)

            countdown_display(f"{int(minutes)}")

            if time_until_next_run <= 0:
                print("Executing scheduled calculation... ")
                schedule.run_pending()
                print("Calculation complete! \n")
    except KeyboardInterrupt:
        print("\nUser interrupted. Exiting gracefully. ")
        sys.exit(0)
 