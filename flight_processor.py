from datetime import datetime
class FlightDataProcessor:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, flights_dct):
        try:
            if isinstance(flights_dct,dict):
                self.flights_dct = flights_dct
            elif isinstance(flights_dct,list):
                self.flights_dct = {}
                for flight in flights_dct:
                    self.flights_dct[flight['flight_number']] = flight 
            else:
                print("Invalid Flight details.. Send list of flights json or dict containing contains flight id as key and whole flight data as its value")
        except:
            print("Invalid Flight Json")
                

    def add_flight(self,data):
        if data['flight_number'] not in self.flights_dct:
            self.flights_dct[data['flight_number']] = data 
        else:
            raise Exception(f"Flight with No-{data['flight_number']} is already present!!")
    
    def remove_flight(self,flight_number):
        if flight_number in self.flights_dct:
            del self.flights_dct[flight_number]
        else:
            raise Exception(f"Flight with No-{flight_number} is not Found!!")
        
    def flights_by_status(self,status):
        l = []
        for i in self.flights_dct:
            if(self.flights_dct[i]['status']==status):
                l.append(self.flights_dct[i])
        return l 
    
    def get_longest_flight(self):
        d = 0
        longest_flight = {}
        for flt in self.flights_dct:
            if(self.flights_dct[flt]["duration_minutes"]>d):
                d = self.flights_dct[flt]["duration_minutes"]
                longest_flight = self.flights_dct[flt]
        return longest_flight
    
    def get_flights(self):
        return list(self.flights_dct.values())
    
    def update_flight_status(self, flight_number: str, new_status: str):
        if flight_number in self.flights_dct:
            self.flights_dct[flight_number]['status'] = new_status
        else:
            raise Exception(f"Flight with No-{flight_number} not found!")
    
'''      
a = FlightDataProcessor([{"flight_number":1,"departure_time":"2025-04-01 10:30","arrival_time":"2025-04-01 10:50","duration_minutes":20,"status":"ON_TIME"},{"flight_number":2,"departure_time":"2025-04-01 11:30","arrival_time":"2025-04-01 11:40","duration_minutes":10,"status":"ON_TIME"},{"flight_number":3,"departure_time":"2025-04-01 11:50","arrival_time":"2025-04-01 11:55","duration_minutes":5,"status":"DELAYED"}])
print(a.get_flights())
print(a.get_longest_flight())

print("Delayed",a.flights_by_status("DELAYED"))
print("-------")
print(a.remove_flight(1))
print(a.get_flights())
'''

"""
Switching to a dict keyed by flight_number (instead of a list of Dicts) for O(1) lookups, additions, and deletions is Efficient in all the below scenarios:

1. Fast add_flight with duplicate check
2. Fast remove_flight
3. Efficient get_longest_flight traversal (still O(n))
"""

"""
Created Singleton Class before but for testing converted into a normal class as 
"""