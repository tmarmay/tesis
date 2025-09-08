from models.route import Route
from random import randint, choice, sample
from itertools import combinations

def neighborhood_definition(kappa: int):
    """
    Define la estructura de vecindad según el valor de kappa, 
    basado en la tabla del paper [1.b].
    """
    table = {
        0: ("intra-depot", 3),
        1: ("intra-depot", 4),
        2: ("intra-depot", 5),
        3: ("intra-depot", 6),
        4: ("inter-depot", 3),
        5: ("inter-depot", 4),
        6: ("inter-depot", 5),
        7: ("inter-depot", 6),
        8: ("inter-depot", 2),
        9: ("intra-depot", 2),
    }
    
    # if kappa not in table:
    #     raise ValueError("kappa debe estar entre 1 y 12")
    
    return table[kappa % 10]

from random import choice, randint

def intra_shaking(neighborhood: list, max_seq_len: int) -> list[Route]:
    if len(neighborhood) == 0:
        raise ValueError("El vecindario no puede estar vacío")
    
    depot = choice(neighborhood)
    route = depot.route

    n = len(route)
    if n <= 1:
        return neighborhood

    for _ in range(max_seq_len):
        i, j = randint(0, n - 1), randint(0, n - 1)
        while i == j:
            j = randint(0, n - 1)
        # swap entre i y j
        route[i], route[j] = route[j], route[i]

    depot.route = route
    return neighborhood



def inter_shaking(neighborhood: list, max_seq_len: int) -> list[Route]:
    if len(neighborhood) == 0:
        raise ValueError("El vecindario no puede estar vacío")

    if len(neighborhood) == 1:
        return neighborhood

    depot1, depot2 = None, None
    while depot1 == depot2:
        depot1 = choice(neighborhood)
        depot2 = choice(neighborhood)

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
            k = len(route1)/2
        
        nodes_to_return = sample(route1, int(k))
        # Los eliminamos de route1
        for node in nodes_to_return:
            route1.remove(node)

        # Y los devolvemos a route2
        route2.extend(nodes_to_return)

    # Actualizamos las rutas de los depósitos
    depot1.route = route1
    depot2.route = route2

    return neighborhood


def generate_all_partition_indices(route, max_seq_len=3):
    n = len(route)
    partitions = []

    # Generar todas las combinaciones posibles de tres índices de corte
    # i < j < k son posiciones donde "rompemos" la ruta
    for i, j, k in combinations(range(1, n), 3):
        # Longitudes de los tres segmentos
        seg1 = j - i
        seg2 = k - j
        seg3 = n - k

        # Chequear que todas las longitudes >= max_seq_len
        if seg1 >= max_seq_len and seg2 >= max_seq_len and seg3 >= max_seq_len:
            partitions.append((i, j, k))

    return partitions

def apply_3opt_no_inversion(route, max_seq_len=3):
    """
    Aplica una variación de 3-opt sin inversión.
    Devuelve la mejor ruta encontrada (o la misma si no mejora).
    """
    n = len(route)
    best_route = route[:]
    best_distance = route_distance(route)

    # Generar todas las combinaciones de tres cortes
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                seg1, seg2, seg3 = route[:i], route[i:j], route[j:k]
                seg4 = route[k:]

                # Restringir por max_seq_len
                if len(seg2) > max_seq_len or len(seg3) > max_seq_len:
                    continue

                # Crear una nueva ruta sin invertir
                new_route = seg1 + seg3 + seg2 + seg4
                new_distance = route_distance(new_route)

                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance

    return best_route

def all_segments(route: list, max_length: int = 3, skip_endpoints: bool = True) -> list:
    """
    Devuelve todos los posibles segmentos como tuplas de índices (i, j)
    que representan route[i:j].
    """
    n = len(route)
    start = 1 if skip_endpoints else 0          # típico: no mover depósitos
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

