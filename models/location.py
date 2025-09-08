from sim_settings import client, DISTANCES_MATRIX_PATH, CITIES_PATH

import pandas as pd
import numpy as np 

class Location():
    cities_df = pd.read_csv(CITIES_PATH)
    dist_df = pd.read_csv(DISTANCES_MATRIX_PATH, index_col=0)
    
    def __init__(self):
        self.place, self.lat, self.lon = self.random_coordinates()
        
    # def calculate_coordinates(self, address):
    #     try:
    #         geocode = client.pelias_search(text=address)
    #         coords = geocode['features'][0]['geometry']['coordinates']
    #         return coords[1], coords[0]  # (lat, lon)
    #     except Exception as e:
    #         print(f"Error al geocodificar {address}: {e}")
    #         return None

    @staticmethod
    def random_coordinates():
        try:
            random_row = Location.cities_df.sample(n=1).iloc[0]  # .iloc[0] es una Series (una fila)
            random_city = random_row['city']
            lat = float(random_row['lat'])
            lng = float(random_row['lng'])
            return random_city, lat, lng
        except:
            return Location.random_coordinates()

    def distance_to_point(self, city2):
        try:
            dist = Location.dist_df.at[self.place, city2]
            # Si dist es una Serie, agarramos el primer valor
            if isinstance(dist, pd.Series):
                dist = dist.iloc[0]
            return round(float(dist),2)
        except KeyError:
            print(f"Una o ambas ciudades '{self.place}' y '{city2}' no están en el archivo de distancias.")
            return 100_000.0


    def get_coordinates(self):
        return self.lat, self.lon
    
        
    def distance_to_point2(self, destination_cord) -> float:
        # Calculate the distance
        try:
            origin_cord = self.get_coordinates()[::-1]
            destination_cord = destination_cord[::-1]
            routes = client.directions(coordinates=[origin_cord, destination_cord], profile='driving-car')['routes']
            distance_in_meters = routes[0]['summary']['distance']
            distance_in_km = distance_in_meters / 1000
            return float("{:.2f}".format(distance_in_km))
        except Exception as e:
            print(f"Error origen {self.place} destination {destination_cord}, {e}")
            return 1_000_000
    
    def get_dij(self, fromm, to):
        distance = self.dist_df[fromm][to]
        if not isinstance(distance, np.floating):
            distance = 1_000_000
        return distance
    
    def get_tij(self, fromm, to):
        return 5 # PENDIENDTE MEJROAR
