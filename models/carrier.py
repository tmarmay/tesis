from models.location import Location

import random
import copy

class Carrier():
    _id_counter = 0

    def __init__(self):
        self.id = f'carrier-{Carrier._id_counter}'
        Carrier._id_counter += 1
        self.location = Location()
        self.available = bool(random.randint(0,2))
        self.km_cost = random.randint(2000, 3500) # se puede mejorar con datos de la paginaS
        self.distance_to_start_assigned = []
        self.parcial_cost = 0
        self.parcial_km = 0
    
    def is_aviable(self):
        self.available

    def get_location(self):
        return self.location.place

    def get_coordinates(self):
        return self.location.get_coordinates()
    
    def get_km_cost(self):
        return self.km_cost
    
    def copy(self):
        return copy.deepcopy(self)
