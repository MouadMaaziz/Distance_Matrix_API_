# Distance Matrix API Scheduler

The Distance Matrix API Scheduler is a robust Python script designed to periodically compute travel distances and durations using the Google Maps Distance Matrix API, taking into account potential changes in road conditions throughout the day. The script accounts for various dynamic factors such as construction sites, traffic congestion, and toll road conditions by scheduling calculations hourly and leveraging the departure_time parameter in API calls.

![Distance Matrix API Visualization](./distance-matrix-google-maps-api.jpg)

## Features

- Automated hourly updates to reflect changing road conditions.
- Support for various travel modes and units of measurement (metric/imperial).
- Caching mechanism to optimize API query efficiency and reduce costs.
- Easy-to-use with an interactive setup prompt.
- Outputs results to a timestamped Excel file for easy tracking and analysis.

## Prerequisites

- Python 3.x
- pandas
- openpyxl (optional, for writing to `.xlsx` format)
- requests

## Getting Started

1. Clone or download this repository to your local machine.
2. Obtain your Google Maps API key and store it securely.
3. Install the required dependencies with the command:
   pip install pandas requests
4. Prepare an input file named input.xlsx with two columns: origin and destination. Fill in your locations.
5. Execute the script, and follow the interactive prompts to set preferences for units and travel mode.