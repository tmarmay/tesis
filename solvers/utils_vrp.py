from models.location import Location
from models.route import Route

L = Location()

def cost(distance_km: float, trip_cost: float, alpha: float = 1, beta: float = 1) -> float:
    """
    Calcula un costo combinado basado en distancia y costo monetario.

    distance_km : distancia total recorrida (km)
    trip_cost   : costo total monetario del viaje
    alpha       : peso de la distancia en el costo final
    beta        : peso del costo monetario en el costo final

    Retorna:
        float: costo combinado
    """
    return round(alpha * distance_km + beta * trip_cost,2)

def check_tw_feasibility(current_time: int, travel_time: int, earliest_time: int, latest_time: int) -> (bool,int):
    eta = current_time + travel_time
    if latest_time < eta:
        return False, 0
    
    if earliest_time <= eta <= latest_time:
        return True, 0
    
    time_until_open = earliest_time - current_time
    wasted_time = max(0, time_until_open - travel_time)
    
    eta = current_time + wasted_time
    if earliest_time <= eta <= latest_time:
        return True, wasted_time
    return False, 0

def check_entire_route_feasibility(route: list[Route]) -> bool:
    if len(route) == 0:
        return False
    
    for r in route:
        # Sim copy the old env
        cpy_carrier = r.carrier.copy()
        cpy_carrier.location = r.depot
        cpy_route = Route(route=[], carrier=cpy_carrier)
        for s in r.route:
            tij = L.get_tij(cpy_carrier.location.place, s.start.place)
            on_time, wasted_time = check_tw_feasibility(cpy_route.current_time, tij, s.earliest_time, s.latest_time)

            if not on_time: #faltaria tener en cuenta la penalidad
                return False
            cpy_route.add_stop(s)
    return True