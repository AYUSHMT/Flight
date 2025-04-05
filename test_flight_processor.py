import unittest
from datetime import datetime
from flight_processor import FlightDataProcessor  # Import your class

# Sample flight data
sample_flights = [
    {"flight_number": "AZ001", "departure_time": "2025-02-19 15:30", "arrival_time": "2025-02-20 03:45", "duration_minutes": 735, "status": "ON_TIME"},
    {"flight_number": "AZ002", "departure_time": "2025-02-21 11:00", "arrival_time": "2025-02-21 16:00", "duration_minutes": 300, "status": "DELAYED"},
]

class TestFlightDataProcessor(unittest.TestCase):
    
    def setUp(self):
        FlightDataProcessor.__instance = None  # Reset singleton
        self.processor = FlightDataProcessor(sample_flights)

    def test_get_flights(self):
        flights = self.processor.get_flights()
        self.assertEqual(len(flights), 2)

    def test_add_flight_success(self):
        new_flight = {"flight_number": "AZ003", "departure_time": "2025-02-22 08:00", "arrival_time": "2025-02-22 12:00", "duration_minutes": 240, "status": "ON_TIME"}
        self.processor.add_flight(new_flight)
        self.assertEqual(len(self.processor.get_flights()), 3)
        self.assertIn("AZ003", [f["flight_number"] for f in self.processor.get_flights()])

    def test_add_duplicate_flight(self):
        with self.assertRaises(Exception) as ctx:
            self.processor.add_flight(sample_flights[0])
        self.assertIn("already present", str(ctx.exception))

    def test_remove_flight_success(self):
        self.processor.remove_flight("AZ001")
        self.assertEqual(len(self.processor.get_flights()), 1)
        self.assertNotIn("AZ001", [f["flight_number"] for f in self.processor.get_flights()])

    def test_remove_flight_not_found(self):
        with self.assertRaises(Exception) as ctx:
            self.processor.remove_flight("UNKNOWN")
        self.assertIn("not Found", str(ctx.exception))

    def test_flights_by_status_on_time(self):
        on_time_flights = self.processor.flights_by_status("ON_TIME")
        self.assertEqual(len(on_time_flights), 1)
        self.assertEqual(on_time_flights[0]["flight_number"], "AZ001")

    def test_flights_by_status_delayed(self):
        delayed_flights = self.processor.flights_by_status("DELAYED")
        self.assertEqual(len(delayed_flights), 1)
        self.assertEqual(delayed_flights[0]["flight_number"], "AZ002")

    def test_flights_by_status_none(self):
        cancelled = self.processor.flights_by_status("CANCELLED")
        self.assertEqual(cancelled, [])

    def test_get_longest_flight(self):
        longest = self.processor.get_longest_flight()
        self.assertEqual(longest["flight_number"], "AZ001")
        self.assertEqual(longest["duration_minutes"], 735)

    def test_constructor_with_dict(self):
        FlightDataProcessor__instance = None 
        input_dict = {
            "AZ001": sample_flights[0],
            "AZ002": sample_flights[1]
        }
        processor = FlightDataProcessor(input_dict)
        self.assertEqual(len(processor.get_flights()), 2)

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            FlightDataProcessor("invalid input")

    def test_invalid_list_structure(self):
        bad_list = [{"invalid_key": "value"}]
        with self.assertRaises(ValueError):
            FlightDataProcessor(bad_list)
    


if __name__ == '__main__':
    unittest.main()
