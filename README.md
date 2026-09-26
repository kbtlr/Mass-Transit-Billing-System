# Mass Transit Billing System
A billing system for a mass transit network that calculates charges based on user journeys between stations in different pricing zones. Designed to be run using Python and pytest 7.1.3, using only csv, sys, collections and datetime libraries.

## File structure
```
/Mass-Transit-Billing-System
├── program.py                      # Calculates billing
├── test_program.py                 # Examines program.py functionality
├── README.md                       # Instructions
│
├── target/
│   ├── zones_file.csv             # Mapping station names to zones
│   └── journey_data.csv           # User journey records
│
└── test/
    ├── test_zones_file.csv        # Test zone mapping
    └── test_journey_data.csv      # Test journey records
```

## Usage
Ensure Python is installed on your machine, then run the program from the command line as follows:

```bash
python program.py <zones_file_path> <journey_data_path> <output_file_path>
```

Example:
```bash
python program.py target/zones_file.csv target/journey_data.csv output.csv
```

## Tests
The repository includes a pytest script for examination of program functionality. Ensure pytest is installed and run:

```bash
pip install -U pytest
pytest --version
pytest -vv
```

## Assumptions
- UTF-8 csv files are provided for the journey data and zone mapping and are complete
- The instructions provided here are followed correctly
- Zone names will be formatted as integers starting from 1
- Pricing within the zones remains fixed
- Assuming no discounted oyster cards/travel cards
