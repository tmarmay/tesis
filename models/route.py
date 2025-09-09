from models.shipment import Shipment
from models.location import Location
from sim_settings import DELTA

from random import randint

L = Location()

class Route():
    def __init__(self, route: list[Shipment], carrier):
        self.route = []
        self.start_times = []
        self.end_times = []
        self.route_coords = []
        self.carrier = carrier
        self.depot = carrier.location
        self.total_km = 0
        self.total_cost = randint(2000, 10000)
        self.current_time = 0
        self.target_history = []
        self.init_route(route)
    
    def init_route(self, route):
        for s in route:
            self.add_stop(s)

    def add_stop(self, shipment: Shipment):
        nstops = len(self.route)
        # Distancia al primer punto de partida y entre ordenes
        if nstops == 0:
            self.total_km += self.carrier.location.distance_to_point(shipment.start.place)
        else:
            previous_shimpent = self.route[nstops-1]
            self.total_km += shipment.start.distance_to_point(previous_shimpent.end.place)
        self.total_km += shipment.distance

        # Tiempo al primer punto de partida, entre ordenes y delta por la carga
        self.current_time +=  self.update_current_time(self.carrier.location, shipment.start, shipment.end)

        self.carrier.location = shipment.end
        self.route.append(shipment)

    def update_current_time(self, carrier_location: str, shipment_start: str, shipment_end) ->int:
        '''
        no devuelve el nuevo current time, sino lo que hay que sumarle
        '''
        new_ctime = L.get_tij(carrier_location, shipment_start)
        
        # Registro que comienza el viaje
        self.start_times.append(self.current_time + new_ctime)
        
        new_ctime += L.get_tij(shipment_start, shipment_end)
        new_ctime += DELTA
        
        # Registro cuando termina el viaje
        self.end_times.append(self.current_time + new_ctime)
        return new_ctime


    def return_routes_names(self):
        return [(s.start.place, s.end.place) for s in self.route]

    def total_route_km(self):
        if len(self.route) == 0:
            km = 0
        
        # Viaje hasta el 
        try:
            km = self.carrier.location.distance_to_point(self.route[0].start.place)
        except: 
            km = 1_000_000
        for r in self.route:
            km += r.get_distance()
            #falta la distancia hasta el depot desp del primero
        return round(km, 2)
    
    def route_cost(self):
        return self.total_km * self.carrier.get_km_cost()