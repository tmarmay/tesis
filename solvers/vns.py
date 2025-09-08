"""
vnsp.py
Solver Variable Neighborhood Search (VNS) for MD-VRP-TW.
"""
from sim_settings import KAPPA, DELTA
from solvers.aux.vns_aux import *
from solvers.utils_vrp import cost, check_entire_route_feasibility
from models.shipment import Shipment
from models.route import Route
from models.carrier import Carrier
from models.location import Location
from solvers.dummy_nnp import mdvrptw_initial_solution

from random import randint, choice
import time 

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


def shaking(old_neighborhood: list[Route], kappa: int = 12) -> list[Route]:
    neighborhood = old_neighborhood.copy()
    # 1. Definir parámetros de vecindad según k
    # import ipdb; ipdb.set_trace()
    depots_involved, max_seq_length = neighborhood_definition(kappa)

    # 2. Elegir rutas según depots_involved
    # if depots_involved == "intra-depot":
    #     new_routes = intra_shaking(neighborhood, max_seq_length)     
    # else:
    new_routes = inter_shaking(neighborhood, max_seq_length)
    return new_routes

def local_search(new_sol: list[Route], isol: list[Route]) -> list[Route]:
    frs_round = True
    improved = True
    while improved:
        improved = False
        for r, cr in zip(new_sol, isol): 
            if frs_round:
                r.target_history.append((r.total_km, r.total_cost))
                frs_round = False

            old_cost = cost(cr.total_km, cr.total_cost)   
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

                    candidate_route = swap_segments(r.route, seg1, seg2, invert=False)
                    candidate_route_instance = Route(route=candidate_route, carrier=r.carrier)
                    
                    # Evaluamos si mejora el costo (y respeta restricciones o penaliza adecuadamente)
                    new_cost = cost(candidate_route_instance.total_km, candidate_route_instance.total_cost)
                    
                    if new_cost < old_cost:
                        if check_entire_route_feasibility([candidate_route_instance]):
                            old_cost = new_cost
                            r.target_history.append((candidate_route_instance.total_km, candidate_route_instance.total_cost))
                            # Aceptamos la mejora
                            r.route[:] = candidate_route
                            # Indicamos que hubo mejora para reiniciar el loop
                            improved = True
                            # Rompemos de esta iteración para reiniciar la búsqueda
                            break
                    if improved:
                        break            
            if improved:
                break
    return new_sol

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

    # Post-Condicion: isol no necesariamente es una solucion factible :list[Route]
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

    first = True
    while not check_entire_route_feasibility(isol) or first:
        first = False
        for k in range(1, KAPPA+1):
            new_sol = shaking(isol, k)
            r = local_search(new_sol, isol)

            # if r != isol: si quiero comparar asi tengo que cambiar la comparacion de las clases (__eq__)
            if check_entire_route_feasibility(r):
                isol = r
                target_history.append((
                    sum(r.total_route_km() for r in isol),
                    sum(r.route_cost() for r in isol)
                ))

        
    end_time = time.perf_counter()
    routes = clean(isol, end_time - start_time, target_history, solved=True)
    return routes



