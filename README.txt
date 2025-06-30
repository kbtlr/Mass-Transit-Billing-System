############################# Mass Transit Billing System

This is a billing system for a mass transit network that calculates charges based on user journeys between stations 
in different pricing zones. Designed to be run using Python, and pytest 7.1.3, using only csv, sys, 
collections and datetime libraries.

############################# Files

/TM_Solution
- 'program.py': Calculates billing.
- 'test_program.py': Examines 'program.py' functionality
- 'README.txt': Instructions on the TM_Solution.zip file usage
/TM_Solution/target
- `zones_file.csv`: A CSV file mapping station names to zones.
- `journey_data.csv`: A CSV file containing user journey records.
/TM_Solution/test
- `test_zones_file.csv`: A CSV file mapping station names to zones.
- `test_journey_data.csv`: A CSV file containing user journey records.

############################# Usage

Ensure Python is installed on your machine, then run the program from the command line as follows:


python program.py <zones_file_path> <journey_data_path> <output_file_path>
python <PATH_TO>\TM_Solution\program.py <PATH_TO>\TM_Solution\target\zone_map.csv <PATH_TO>\TM_Solution\target\journey_data.csv <PATH_TO>\TM_Solution\output.csv


Append the <PATH_TO> sections with your own directories to the file.


############################# Tests

The .zip file comes equipped with a pytest script for examination of .py file functionality. 
Ensure the pytest library performs as necessary by entering the following:

pip install -U pytest
pytest --version
pytest <PATH_TO>\TM_Solution\ -vv


############################# Assumptions

UTF-8 csv files are provided for the journey data and zone mapping and are complete
The instructions provided here are followed correctly
Zone names will be formatted as integers starting from 1.
Pricing within the zones remains fixed.
Assuming no discounted oyster cards/travel cards