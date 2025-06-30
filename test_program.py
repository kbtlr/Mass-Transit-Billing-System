# A pytest program designed to examine and debug functionality of a mass transit system using .csv data implemented
# as fixtures
import tempfile
from pathlib import Path
import csv
import pytest
# Important functions imported from the mass transit .py script
from program import load_zones, calculate_journey_cost, calculate_billing, write_output, main


# The following fixtures mimic .csv data as used in the main script while maintaining minimal overhead
@pytest.fixture
def test_zone_map():
    return {
        "station1": 1,
        "station2": 2,
        "station3": 3,
        "station4": 4,
    }


# Original dataset tests caps, so this one was designed to test IN/OUT matches
@pytest.fixture
def test_journey_data():
    return [
        ("user1", "IN", "station1", "2024-10-01T11:40:00"),
        ("user2", "IN", "station3", "2024-10-01T11:50:00"),
        ("user3", "IN", "station1", "2024-10-01T11:55:00"),
        ("user1", "OUT", "station3", "2024-10-01T13:55:00"),
        ("user2", "IN", "station4", "2024-10-03T06:30:00"),
        ("user2", "OUT", "station2", "2024-10-03T09:51:25"),
        ("user1", "IN", "station1", "2024-10-07T10:20:00"),
        ("user1", "OUT", "station1", "2024-10-11T10:20:05"),
        ("user3", "OUT", "station2", "2024-10-15T08:10:00"),
        ("user2", "IN", "station2", "2024-10-15T08:25:00"),
        ("user1", "OUT", "station2", "2024-10-15T11:30:00")
    ]


# Temporary .csv file is designed to test load_zones() functionality, and output is tested against
# assertions
def test_load_zones():
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_file_path = Path(tmpdirname) / "test_zones.csv"
        with temp_file_path.open("w", encoding="utf-8", newline="") as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(["Z", "zone"])
            writer.writerows([
                ["station1", "1"],
                ["station2", "2"],
                ["station3", "3"],
                ["station4", "4"]
            ])

        zone_map = load_zones(temp_file_path)
        assert zone_map == {
            "station1": 1,
            "station2": 2,
            "station3": 3,
            "station4": 4,
        }


# calculate_journey_cost() tested against assertions, with the approx function avoiding float deviations
def test_calculate_journey_cost():
    assert calculate_journey_cost(1, 2) == pytest.approx(3.30, 0.01)  # BASE + 0.80 + 0.50
    assert calculate_journey_cost(1, 4) == pytest.approx(3.10, 0.01)  # BASE + 0.80 + 0.30
    assert calculate_journey_cost(3, 6) == pytest.approx(2.60, 0.01)  # BASE + 0.50 + 0.10


# Fixtures provide data for the calculate_billing() function, once again asserting approximated results
def test_calculate_billing(test_journey_data, test_zone_map):
    billing_results = calculate_billing(test_journey_data, test_zone_map)
    expected_results = {
        "user1": pytest.approx(18.30, 0.01),
        "user2": pytest.approx(12.80, 0.01),
        "user3": pytest.approx(10.00, 0.01),
    }
    assert billing_results == expected_results


# .csv output format is tested against the main scripts formatting, ensuring data compatibility
def test_write_output():
    results = {
        "user1": 18.30,
        "user2": 12.80,
        "user3": 10.00,
    }
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_file_path = Path(tmpdirname) / "test_output.csv"
        write_output(temp_file_path, results)
        # Correct encoding and header formatting, then asserted
        with temp_file_path.open("r", encoding="utf-8") as temp_file:
            reader = csv.reader(temp_file)
            header = next(reader)
            assert header == ["user_id", "total"]
            output = list(reader)
            expected_output = [
                ["user1", "18.30"],
                ["user2", "12.80"],
                ["user3", "10.00"]
            ]
            assert output == expected_output


# Complete script tested from beginning to end, generating temporary data for formatting and outputting
# as a utf-8 .csv file, and ratified with assertions
def test_main_end_to_end(test_zone_map, test_journey_data):
    with tempfile.TemporaryDirectory() as tmpdirname:
        zone_file_path = Path(tmpdirname) / "test_zones.csv"
        journey_file_path = Path(tmpdirname) / "test_journeys.csv"
        output_file_path = Path(tmpdirname) / "test_output.csv"

        with zone_file_path.open("w", encoding="utf-8", newline="") as zone_file:
            writer = csv.writer(zone_file)
            writer.writerow(["Z", "zone"])
            for station, zone in test_zone_map.items():
                writer.writerow([station, zone])

        with journey_file_path.open("w", encoding="utf-8", newline="") as journey_file:
            writer = csv.writer(journey_file)
            writer.writerow(["user_id", "direction", "station", "time"])
            writer.writerows(test_journey_data)

        main(zone_file_path, journey_file_path, output_file_path)

        with output_file_path.open("r", encoding="utf-8") as output_file:
            reader = csv.reader(output_file)
            header = next(reader)
            assert header == ["user_id", "total"]
            output = list(reader)
            expected_output = [
                ["user1", "18.30"],
                ["user2", "12.80"],
                ["user3", "10.00"]
            ]
            assert output == expected_output
