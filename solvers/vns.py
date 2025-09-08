"""
vnsp.py
Solver Variable Neighborhood Search (VNS) for MD-VRP-TW.
"""
from sim_settings import KAPPA, DELTA, MAX_TRIALS_SHAKING
from solvers.aux.vns_aux import *
from solvers.utils_vrp import cost, check_entire_route_feasibility
from models.shipment import Shipment
from models.route import Route
from models.carrier import Carrier
from models.location import Location
from solvers.dummy_nnp import mdvrptw_initial_solution

from random import randint, choice
import time 
from typing import List, Tuple
import copy 

L = Location()
# ====== Initial Solution ======
def initial_solution(carriers: list, shipments: list) -> list[Route]:
    neighborhood = {}
    insol = []
    #1.each customer i is first assigned to the nearest depot
    closest_carrier, min_distance = None, 1_000_000_000
    for shipment in shipments:
        for carrier in carriers:
            distance =  L.get_dij(carrier.location.place, shipment.start.place)
            if distance < min_distance:
                min_distance = distance
                closest_carrier = carrier
        shipment.closest_carrier = closest_carrier
        
        if not neighborhood.get(closest_carrier, False):
            neighborhood[closest_carrier] = []
        tw_center = (shipment.earliest_time + shipment.latest_time) / 2
        neighborhood[closest_carrier].append((shipment, tw_center))
    #2. all customers within a depot are ordered by the center of their time window
    for key, value in neighborhood.items():
        sorted_value = sorted(value, key=lambda x: x[1])
        # Eliminar la segunda entrada y construir las Rutas
        insol.append(Route(route=[shipment for shipment, _ in sorted_value], carrier=key))
    return insol


def shaking(current_solution: list[Route], kappa: int, max_trials: int = MAX_TRIALS_SHAKING) -> Tuple[bool, List[Route], List[int]]:
    neighborhood = copy.deepcopy(current_solution)
    # 1. Definir parámetros de vecindad según k
    is_feasible = False
    trial = 0
    while not is_feasible and trial < max_trials:
        depots_involved, max_seq_length = neighborhood_definition(kappa)

        # 2. Elegir rutas según depots_involved
        if depots_involved == "intra-depot":
            new_routes, modified_indices = intra_shaking(neighborhood, max_seq_length)
        else:
            new_routes, modified_indices = inter_shaking(neighborhood, max_seq_length)

        is_feasible = check_entire_route_feasibility(new_routes)
        trial += 1

    if is_feasible:
        return True, new_routes, modified_indices # mejoro
    
    return False, neighborhood, modified_indices # devuelvo la misma

def local_search(new_sol: list[Route], isol: list[Route], modified_indices: list[int]) -> list[Route]:
    optimized = False
    improved = True
    while improved:
        improved = False

        # solo tengo que hacerlo en las rutas que se modificaron
        for idx in modified_indices:
            r = new_sol[idx]
            cr = isol[idx]

            current_cost = cost(cr.total_km, cr.total_cost) if not improved else cost(r.total_km, r.total_cost)
             
            # Extraemos todos los segmentos posibles dentro del límite de 3 nodos
            for seg1 in all_segments(r.route, max_length=3):
                for seg2 in all_segments(r.route, max_length=3):
                    if seg1 == seg2:
                        continue

                    # Descartar segmentos que se solapan
                    i1, j1 = seg1
                    i2, j2 = seg2
                    if j1 > i2 and j2 > i1:
                        continue

                    candidate_route = swap_segments(copy.deepcopy(r.route), seg1, seg2, invert=False)
                    candidate = Route(route=candidate_route, carrier=r.carrier)
                    
                    # Evaluamos si mejora el costo (y respeta restricciones o penaliza adecuadamente)
                    new_cost = cost(candidate.total_km, candidate.total_cost)
                    if new_cost < current_cost and check_entire_route_feasibility([candidate]):
                        # Aceptamos la mejora
                        new_sol[idx] = candidate
                        improved = True
                        optimized = True
                        break
                if improved:
                    break
            if improved:
                break
    return optimized, new_sol

def clean(routes: dict, computation_time: float, target_history: list, solved: bool) -> dict:
    result = {}
    result['target_history'] = []
    for r in routes:
        result[r.carrier.id] = {
            'km': r.total_km,
            'cost': r.total_cost,
            'route': r.return_routes_names(),
            'carrier depot': r.depot.place,
            # 'route_coords': [(s.start.get_coordinates(), s.end.get_coordinates()) for s in r.route],
            'relative_time': r.current_time,   
        }

    result['target_history'] = target_history
    result['solved'] = solved
    result['computation_time'] = computation_time
    return result

# ====== Main Function ======
def mdvrptw_solver(carriers: list, shipments: list, sol:list[Route] = None): 
    target_history = []
    start_time = time.perf_counter()

    #isol = initial_solution(carriers, shipments)
    isol = mdvrptw_initial_solution(carriers, shipments)

    if len(isol) == 0:
        solved = False
        end_time = time.perf_counter()
        routes = clean(isol, end_time - start_time, [], solved)
        return routes
    
    target_history.append((
        sum(r.total_route_km() for r in isol),
        sum(r.route_cost() for r in isol)
    ))


    for k in range(1, KAPPA+1):
        improve, new_sol, modified_indices = shaking(isol, k)
        
        if not improve:
            continue
        
        optimized, new_sol = local_search(new_sol, isol, modified_indices)

        if not optimized:
            continue

        if sum(r.total_route_km() for r in new_sol) < sum(r.total_route_km() for r in isol):
            isol = new_sol
            target_history.append((
                sum(r.total_route_km() for r in isol),
                sum(r.route_cost() for r in isol)
            ))

    end_time = time.perf_counter()
    routes = clean(isol, end_time - start_time, target_history, solved=True)
    return routes



