N = 50
M = 20

DISTANCES_MATRIX_PATH = '/Users/tomasmarmay/Documents/profile/famaf/tesis/data/distance_matrix.csv'
TIMES_MATRIX_PATH = '/Users/tomasmarmay/Documents/profile/famaf/tesis/data/distance_matrix.csv' #calular
CITIES_PATH = '/Users/tomasmarmay/Documents/profile/famaf/tesis/data/argentina_ciudades_coordenadas.csv'

import openrouteservice
OPEN_ROUTE_SERVICE_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImZlMzJjNjBkOGFiYzQwYTM4MGY3NDJiNDZlMzRkZWIxIiwiaCI6Im11cm11cjY0In0="
OPEN_ROUTE_SERVICE_CLIENT = openrouteservice.Client(key=OPEN_ROUTE_SERVICE_API_KEY)
client = OPEN_ROUTE_SERVICE_CLIENT

# Tiempo de carga 
DELTA = 0

#VNS
KAPPA = 10