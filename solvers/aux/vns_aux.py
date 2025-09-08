from models.route import Route

from random import randint, choice, sample
from typing import Tuple

def neighborhood_definition(kappa: int):
    """
    Define la estructura de vecindad según el valor de kappa, 
    basado en la tabla del paper [1.b].
    """
    table = {
        1: ("intra-depot", 2),
        2: ("intra-depot", 3),
        3: ("intra-depot", 4),
        4: ("intra-depot", 5),
        5: ("intra-depot", 6),
        6: ("intra-depot", 10000),
        7: ("inter-depot", 2),
        8: ("inter-depot", 3),
        9: ("inter-depot", 4),
        10: ("inter-depot", 5),
        11: ("inter-depot", 6),
        12: ("inter-depot", 10000),
    }
        
    return table[kappa]

from random import choice, randint

def intra_shaking(neighborhood: list, max_seq_len: int) -> Tuple[list[Route], list[int]]:
    if len(neighborhood) == 0:
        raise ValueError("El vecindario no puede estar vacío")
    
    index = randint(0, len(neighborhood) - 1)
    depot = neighborhood[index]
    route = depot.route

    n = len(route)
    if n <= 1:
        return neighborhood, []

    if max_seq_len > len(route):
        max_seq_len = len(route) - 1

    for _ in range(max_seq_len):
        i, j = randint(0, n - 1), randint(0, n - 1)
        while i == j:
            j = randint(0, n - 1)
        # swap entre i y j
        route[i], route[j] = route[j], route[i]

    depot.route = route
    return neighborhood, [index]



def inter_shaking(neighborhood: list, max_seq_len: int) -> Tuple[list[Route], list[int]]:
    if len(neighborhood) == 0:
        raise ValueError("El vecindario no puede estar vacío")

    if len(neighborhood) == 1:
        return neighborhood, []

    i1, i2 = sample(range(len(neighborhood)), 2)  # elige 2 índices distintos
    depot1 = neighborhood[i1]
    depot2 = neighborhood[i2]

    route1 = depot1.route
    route2 = depot2.route

    # Aseguramos que route1 sea la más larga
    if len(route1) < len(route2):
        route1, route2 = route2, route1
        depot1, depot2 = depot2, depot1

    # Guardamos los nodos a transferir de la ruta más corta
    transferred_nodes = route2.copy()

    # Transferimos todos los nodos a la ruta más larga
    route1 += transferred_nodes
    route2.clear()

    # Seleccionamos aleatoriamente hasta max_seq_len nodos para devolverlos
    k = max_seq_len #, len(transferred_nodes)
    if k > 0:
        if k > len(route1):
            k = len(route1)
        
        nodes_to_return = sample(route1, int(k))
        # Los eliminamos de route1
        for node in nodes_to_return:
            route1.remove(node)

        # Y los devolvemos a route2
        route2.extend(nodes_to_return)

    # Actualizamos las rutas de los depósitos
    depot1.route = route1
    depot2.route = route2

    return neighborhood, [i1, i2]


def all_segments(route: list, max_length: int = 3, skip_endpoints: bool = False) -> list:
    """
    Devuelve todos los segmentos contiguos posibles de la lista,
    con longitud máxima = max_length.

    Cada segmento se representa como (i, j], que corresponde a route[i:j].
    """

    n = len(route)
    start = 1 if skip_endpoints else 0
    end   = n - 1 if skip_endpoints else n
    out = []
    for i in range(start, end):
        for L in range(1, min(max_length, end - i) + 1):
            out.append((i, i + L))  # (inicio, fin)
    return out

def swap_segments(route: list, seg1: tuple, seg2: tuple, invert: bool=False) -> list:
    """
    Intercambia dos segmentos dentro de una ruta sin duplicar elementos.
    Los segmentos no deben solaparse.
    """
    i1, j1 = seg1
    i2, j2 = seg2

    # Asegurarse de que i1 < i2 para simplificar reconstrucción
    if i2 < i1:
        i1, j1, i2, j2 = i2, j2, i1, j1

    # Revisar que no se solapen
    if j1 > i2:
        return route  # segmentos solapados, no intercambiar

    part1 = route[i1:j1]
    part2 = route[i2:j2]

    if invert:
        part1 = list(reversed(part1))
        part2 = list(reversed(part2))

    new_route = (
        route[:i1] +
        part2 +
        route[j1:i2] +
        part1 +
        route[j2:]
    )
    return new_route

