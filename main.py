import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import schedule
import time
import itertools
import logging
from dotenv import load_dotenv
from distance_matrix_api import get_distance_matrix
from parse_duration import duration_to_delta

load_dotenv()  # Load environment variables from a .env file

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the API key from an environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
UNIT = 'metric'
TRAVEL_MODE = 'fastest'

# Set some global configurations
SCHEDULE_INTERVAL_HOURS = 1
INPUT_FILE = 'input.xlsx'
OUTPUT_FILE_PATTERN = 'output_{timestamp}.xlsx'

def get_output_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_at_%H_%M_%S")
    return OUTPUT_FILE_PATTERN.format(timestamp=timestamp)


def scheduled_calculation():
    try:
        # Load data from the input file
        data = pd.read_excel(INPUT_FILE)

        # Results lists
        distances = []
        durations = []
        modes = []

        for i, row in data.iterrows():
            origin = row['origin']
            destination = row['destination']
            timestamp = int(time.time())

            results = get_distance_matrix(API_KEY, origin, destination, UNIT, TRAVEL_MODE, timestamp)
            if results:
                # Assume the fastest one is the one with the shortest duration
                fastest = min(results, key=lambda x: duration_to_delta(x['duration']).total_seconds())

                distances.append(fastest['distance'])
                durations.append(fastest['duration'])
                modes.append(fastest['mode'])
            else:
                distances.append(None)
                durations.append(None)
                modes.append(None)
                logging.warning(f"No results for {origin} to {destination}")

        # Add the new columns to the DataFrame
        now = datetime.now()
        data['distance'] = distances
        data['duration'] = durations
        data['departure_time'] = now.strftime("%Y-%m-%d %H:%M:%S")
        data['mode'] = modes

        # Calculating and formatting the arrival time
        data['arriving_time'] = [now + duration_to_delta(duration) if duration else None for duration in durations]

        # Save the results
        new_output_file = get_output_filename()
        data.to_excel(new_output_file, index=False)
        logging.info(f"Created {new_output_file}")

    except Exception as e:
        logging.exception("An error occurred during the scheduled calculation.")

def countdown_display(minutes):
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    while minutes > 0:
        sys.stdout.write("\rNext execution in {:02.0f}:{:02.0f} minutes {}".format(*divmod(minutes * 60, 60), next(spinner)))
        sys.stdout.flush()
        time.sleep(1)
        minutes -= 1 / 60
    sys.stdout.write("\r")

if __name__ == '__main__':
    
    logging.info("Starting the Auto Distance and Time Calculator.")
    
    if not API_KEY:
        logging.error("No API key found. Please set the GOOGLE_MAPS_API_KEY environment variable.")
        sys.exit(1)

    schedule.every(SCHEDULE_INTERVAL_HOURS).hours.do(scheduled_calculation)

    # Initial run
    scheduled_calculation()

    try:
        while True:
            minutes_until_next_run = schedule.idle_seconds() / 60
            countdown_display(minutes_until_next_run)
            schedule.run_pending()
    except KeyboardInterrupt:
        logging.info("User interrupted the process. Exiting gracefully.")
        sys.exit(0)