import unittest
from flight_processor import FlightDataProcessor  # Your class file

flight_data = [
    {"flight_number": "AZ001", "departure_time": "2025-02-19 15:30", "arrival_time": "2025-02-20 03:45", "duration_minutes": 735, "status": "ON_TIME"},
    {"flight_number": "AZ002", "departure_time": "2025-02-21 11:00", "arrival_time": "2025-02-21 16:00", "duration_minutes": 300, "status": "DELAYED"},
]

class TestFlightDataProcessor(unittest.TestCase):

    def setUp(self):
        # This runs before each test
        #FlightDataProcessor.__instance = None  # Reset singleton
        self.processor = FlightDataProcessor(flight_data)

    def test_get_flights(self):
        self.assertEqual(len(self.processor.get_flights()), 2)

    def test_add_flight(self):
        new_flight = {"flight_number": "AZ003", "departure_time": "2025-02-22 10:00", "arrival_time": "2025-02-22 14:00", "duration_minutes": 240, "status": "ON_TIME"}
        self.processor.add_flight(new_flight)
        self.assertIn("AZ003", [f["flight_number"] for f in self.processor.get_flights()])

    def test_duplicate_flight_addition(self):
        with self.assertRaises(Exception):
            self.processor.add_flight(flight_data[0])  

    def test_remove_flight(self):
        self.processor.remove_flight("AZ001")
        self.assertEqual(len(self.processor.get_flights()), 1)

    def test_remove_invalid_flight(self):
        with self.assertRaises(Exception):
            self.processor.remove_flight("AZ999")

    def test_flights_by_status(self):
        delayed = self.processor.flights_by_status("DELAYED")
        self.assertEqual(len(delayed), 1)
        self.assertEqual(delayed[0]["flight_number"], "AZ002")

    def test_get_longest_flight(self):
        longest = self.processor.get_longest_flight()
        self.assertEqual(longest["flight_number"], "AZ001")

if __name__ == '__main__':
    unittest.main()
