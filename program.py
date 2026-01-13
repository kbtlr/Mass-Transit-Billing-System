# A mass transit billing system designed using only Python native libraries on a Windows 64-bit system
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Set global beans for use later in the algorithm
BASE = 2.00
DAILY_CAP = 15.00
MONTHLY_CAP = 100.00
PENALTY = 5.00

PRICES = {
    1: 0.80,
    2: 0.50,
    3: 0.50,
    4: 0.30,
    5: 0.30,
    6: 0.10,
}

# Reads .csv file for zone mappings, returning a list
def load_zones(file_path: Path) -> Dict[str, int]:
    zone_map = {}
    with file_path.open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            station = row['Z'].strip()
            zone = int(row['zone'].strip())
            zone_map[station] = zone
    return zone_map


# Handling of zone edge cases
def validate_zones(zone_map):
    for station, zone in zone_map.items():
        if not (1 <= zone <= 6):
            print(f"Error: Zone '{zone}' for station '{station}' is outside the allowed range (1-6).")
            sys.exit(1)


# Computes entry and exit costs based on the global constraints listed above
def calculate_journey_cost(entry_zone: int, exit_zone: int) -> float:
    cost = BASE + PRICES.get(entry_zone, 0) + PRICES.get(exit_zone, 0)
    return cost


# Quality of life functions to make fee application easier to debug
def apply_daily_cap(current_total: float, journey_cost: float) -> float:
    if current_total + journey_cost > DAILY_CAP:
        return DAILY_CAP - current_total
    return journey_cost


def apply_monthly_cap(total: float) -> float:
    return min(total, MONTHLY_CAP)


# Provides data on the journeys of each individual user, such as IN/OUT entries.
def calculate_billing(journey_data: List[Tuple[str, str, str, str]], zone_map: Dict[str, int]) -> Dict[str, float]:
    # Initialize billing data
    billing_data = defaultdict(lambda: {
        'total': 0.0,
        'unmatched_ins': [],
        'daily_totals': defaultdict(float),
        'monthly_total': 0.0
    })
    # Process each journey
    for user_id, direction, station, timestamp in journey_data:
        zone = zone_map.get(station.strip())
        date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").date()

        # Process each journey: Match INs and OUTs. If no match, a fee is applied
        if direction == "IN":
            billing_data[user_id]['unmatched_ins'].append((zone, date))

        elif direction == "OUT" and billing_data[user_id]['unmatched_ins']:
            for i, (entry_zone, entry_date) in enumerate(billing_data[user_id]['unmatched_ins']):
                if entry_date == date:
                    journey_cost = calculate_journey_cost(entry_zone, zone)
                    daily_total = billing_data[user_id]['daily_totals'][date]
                    capped_cost = apply_daily_cap(daily_total, journey_cost)
                    billing_data[user_id]['total'] += capped_cost
                    billing_data[user_id]['daily_totals'][date] += capped_cost
                    billing_data[user_id]['unmatched_ins'].pop(i)
                    break
            else:
                billing_data[user_id]['total'] += PENALTY

    for user_id, data in billing_data.items():
        total_penalties = PENALTY * len(data['unmatched_ins'])
        monthly_total = sum(data['daily_totals'].values()) + total_penalties
        data['total'] = apply_monthly_cap(data['total'] + total_penalties)

    return {user_id: round(data['total'], 2) for user_id, data in billing_data.items()}


# Creates an output file with users and monthly bills totaled to 2 decimal places as asked
def write_output(output_file_path: Path, results: Dict[str, float]) -> None:
    with output_file_path.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'total'])  # Add headers for clarity
        for user_id, bill in sorted(results.items()):
            writer.writerow([user_id, f"{bill:.2f}"])


# Main execution which takes as input the filepaths entered into the command prompt (In that order),
# and uses them as the paths for the aforementioned .csv files.
def main(zones_file_path: str, journey_data_path: str, output_file_path: str) -> None:
    zone_map = load_zones(Path(zones_file_path))
    validate_zones(zone_map)  # Validate zones before proceeding
    with Path(journey_data_path).open('r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        journey_data = [(row['user_id'], row['direction'], row['station'], row['time']) for row in reader]

    results = calculate_billing(journey_data, zone_map)
    write_output(Path(output_file_path), results)


# A failsafe to prevent any more than 4 arguments being taken as a command:
# The .py file and the .csv files
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Format input as follows: python my_solution.py <zones_file_path> <journey_data_path> <output_file_path>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
