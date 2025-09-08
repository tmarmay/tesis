"""
dummy_nnp.py
Solver Nearest Neighbor Path (NNP) for MD-VRP-TW.
Dummy version.
"""
from solvers.utils_vrp import check_tw_feasibility
from models.location import Location
from sim_settings import DELTA
from models.route import Route

import time 

L = Location()
# ====== Main Function ======
def mdvrptw_solver(carriers: list, shipmentss: list): 
    shipments = shipmentss.copy()
    start_time = time.perf_counter()
    result = {}
    result['km'] = 0
    result['cost'] = 0
    result['sol'] = []
    for carrier in carriers:
        r = Route([], carrier)
        carrier_full = False
        
        while len(shipments) != 0:
            next_shipment = select_nearest_feasible_shipment(r.current_time, r.carrier.location.place, shipments)

            if next_shipment is None:
                carrier_full = True
                break
            
            r.add_stop(next_shipment)
            
            # Eliminar el shipment asignado
            shipments.remove(next_shipment)

        if len(r.route) > 0:
            result[carrier.id] = {
                'km': r.total_km,
                'cost': r.total_cost,
                'route': r.return_routes_names(),
                'carrier depot': r.depot.place,
                # 'route_coords': route_coords,
                'relative_time': r.current_time,
            }
            result['km'] += r.total_km
            result['cost'] += r.total_cost
            result['sol'].append(r)

        if carrier_full:
            continue
        
    if len(shipments) > 0:
        result['solved'] = False
    else:
        result['solved'] = True

    end_time = time.perf_counter()
    result['computation_time'] = end_time - start_time
    result['target_history'] = []
    return result


# ====== Selección del envío más cercano y factible ======
def select_nearest_feasible_shipment(current_time, carrier_location, shipments):
    feasible_shipments = []
    
    for shipment in shipments:
        tij = L.get_tij(carrier_location, shipment.start.place)
        on_time, wasted_time = check_tw_feasibility(current_time, tij, shipment.earliest_time, shipment.latest_time)
        if on_time and wasted_time == 0:
            feasible_shipments.append(shipment)

    # Calcular distancias y seleccionar el más cercano
    if len(feasible_shipments) > 0:
        shipments_distances = []
        
        for shipment in feasible_shipments:
            distance = L.get_dij(carrier_location, shipment.start.place)
            shipments_distances.append((shipment, distance))
        
        closest_shipment, _ = min(shipments_distances, key=lambda x: x[1])
        return closest_shipment

    #Capaz hay uno pero tengo que esperar, dentre ellos eligo el mas cercano
    penalty_feasible_shipments = []
        
    for shipment in shipments:
        distance = L.get_dij(carrier_location, shipment.start.place)
        penalty_feasible_shipments.append((shipment, distance))
    
    while len(penalty_feasible_shipments) != 0:
        closest_shipment, distance = min(penalty_feasible_shipments, key=lambda x: x[1])
        tij = L.get_tij(carrier_location, shipment.start.place)
        on_time, wasted_time = check_tw_feasibility(current_time, tij, closest_shipment.earliest_time, closest_shipment.latest_time) 
        if on_time:
            return closest_shipment
        
        if (closest_shipment, distance) in penalty_feasible_shipments:
            penalty_feasible_shipments.remove((closest_shipment, distance))
    return None

# ====== Main Function ======
def mdvrptw_initial_solution(carriers: list, shipmentss: list) -> list[Route]: 
    shipments = shipmentss.copy()
    result = []
    
    for carrier in carriers:
        r = Route([], carrier)
        carrier_full = False
        
        while len(shipments) != 0:
            next_shipment = select_nearest_feasible_shipment(r.current_time, r.carrier.location.place, shipments)

            if next_shipment is None:
                carrier_full = True
                break
            
            r.add_stop(next_shipment)
            
            # Eliminar el shipment asignado
            shipments.remove(next_shipment)

        if len(r.route) > 0:
            result.append(r)

        if carrier_full:
            continue
        
    if len(shipments) > 0:
        return []
    return result