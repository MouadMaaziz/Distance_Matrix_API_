# Distance_Matrix_API
Python script that uses the Pandas library to read data from an Excel file, makes requests to the Google Maps Distance Matrix API to retrieve distance and duration information between origins and destinations, caches API responses for efficiency, and saves the results to an output Excel file. This way both the number of API requests and associated costs are reduced.


![Image Alt Text](./distance-matrix-google-maps-api.jpg)





## Requirements
- Python 3.x
- pandas
- openpyxl (if you want to write the output in .xlsx format)
- requests (if the input files are in .xls format)


## Usage

</br>1. Clone or download this repository to your local machine.

</br>2. Obtain a Google Maps API key and save it in a text file named "your_secret_api_key.txt" in the same directory as the script.

</br>3. Install the required dependencies by running the command
> pip install pandas requests

</br>4. Create an input Excel file named 'input.xlsx' in the same directory as the script, and add a sheet named Sheet1 with two columns: origin and destination. Enter the addresses you want to calculate the distances and durations for in these columns.


</br>5. Run the script
> python distance_matrix_api.py

</br>6. The script will output the results to a new Excel file named output.xlsx in the same directory.


## Caching
To avoid sending unnecessary API requests, the script implements caching of the API responses using a simple dictionary stored in a JSON file named 'cache.json'. If a response has already been cached for a particular origin and destination address pair, the script will return the cached response instead of sending a new API request.


## Contributing
If you find a bug or have a feature request, please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
