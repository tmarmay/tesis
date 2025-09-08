from models.location import Location

import time
import random

class Shipment():
    _id_counter = 0

    def __init__(self):
        self.id = f'carrier-{Shipment._id_counter}'
        Shipment._id_counter += 1
        self.start = Location() 
        self.end = Location()
        self.earliest_time, self.latest_time = self.assign_random_time_window()
        self.distance = self.get_distance()
        self.closest_carrier = None
        
    def get_distance(self):        
        distance = self.start.distance_to_point(self.end.place)
        return round(distance,2)

    def assign_random_time_window(self):
        ei = 0 #random.randint(0, 15)
        li = ei + random.randint(7, 30)
        return ei, li 
    
    def get_start_coordinates(self):
        return self.start.get_coordinates()
    
    def get_end_coordinates(self):
        return self.end.get_coordinates()