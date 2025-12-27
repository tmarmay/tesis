"""
aco.py
Solver Ant Colony System for MD-VRP-TW.
3.c.1 version.
"""
import numpy as np
import random


# =============================
# Parámetros del algoritmo
# =============================
NUM_ANTS = 10
NUM_ITER = 100
ALPHA = 1.0       # influencia de la feromona
BETA = 5.0        # influencia de la heurística (1/distancia)
RHO = 0.5         # tasa de evaporación
Q = 100           # cantidad de feromona depositada
NUM_DEPOTS = 1    # por ahora, un depósito
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# =============================
# Datos de ejemplo
# =============================

# Coordenadas del depósito y clientes
V = 2 # Vehicles = Depots
CUSTOMERS = 2
N = CUSTOMERS + V # por el momento con el mismo depot y return

C = [i for i in range(CUSTOMERS)] #CUSTOMERS
DEPOTS = [i for i in range(C[-1] + 1, C[-1] + 1 + V)]
RETURNS = { #no me gusta porq difiere de milp, verificar mas adalente
    DEPOTS[v]: C[-1] + 1 + V + v
    for v in range(V)
}

#la matriz tiene que ser espejo con la diagonal porque no es dirigido
# para decir que no puedo ir de i a j: Poner 0 en eta[i][j] y/o tau[i][j] va a hacer que la prob sea 0
cost_matrix = np.array([
# 0   1   2   3   4   5   6
[99, 12,  5,  7,  9,  8, 13],  # 0 depot v0
[12, 99,  7,  1,  6, 13,  8],  # 1 depot v1

[ 5,  7, 99,  4,  6,  5,  7],  # 2 cliente 0
[ 7,  1,  4, 99,  5,  7,  5],  # 3 cliente 1
[ 9,  6,  6,  5, 99,  6,  4],  # 4 cliente 2

[ 8, 13,  5,  7,  6, 99, 11],  # 5 return v0
[13,  8,  7,  5,  4, 11, 99],  # 6 return v1
])

F = [5 for _ in range(V)] # penalizacion por usar auto

tij = np.array([
# 0   1   2   3   4   5   6
[99, 10,  4,  6,  8,  7, 12],  # 0 depot v0
[10, 99,  6,  1,  5, 12,  7],  # 1 depot v1

[ 4,  6, 99,  3,  5,  4,  6],  # 2 cliente 0
[ 6,  1,  3, 99,  4,  6,  4],  # 3 cliente 1
[ 8,  5,  5,  4, 99,  5,  3],  # 4 cliente 2

[ 7, 12,  4,  6,  5, 99, 10],  # 5 return v0
[12,  7,  6,  4,  3, 10, 99],  # 6 return v1
])

ei = np.array([
    0,   # depot 0
    0,   # depot 1

    5,   # cliente 0
    0,   # cliente 1
   10,   # cliente 2

    0,   # return v0
    0    # return v1
])

li = np.array([
  999,  # depot 0
  999,  # depot 1

   20,  # cliente 0
   15,  # cliente 1
   30,  # cliente 2

  999,  # return v0
  999   # return v1
])
# =============================
# Inicialización de feromonas
# =============================
tau_assign = np.ones((V, CUSTOMERS)) # Feromonas a los clientes
best_route = None
best_cost = float("inf") #Tiene que evaluar igual que objective_rule de milp 

def select_depot_for_client(c, tau_assign, cost_matrix, depot_nodes):
    numeradores = []
    for d_idx, d_node in enumerate(depot_nodes):

        tau_dc = tau_assign[d_idx][c] ** ALPHA
        eta_dc = (1 / cost_matrix[d_node][c]) ** BETA

        numeradores.append(tau_dc * eta_dc)

    total = sum(numeradores)
    if total == 0:
        return random.choice(range(len(depot_nodes)))

    probs = [n / total for n in numeradores]

    # devolvés el índice del depósito
    return random.choices(range(len(depot_nodes)), weights=probs, k=1)[0]


def assignment_phase(C, DEPOTS, tau_assign, cost_matrix):
    assign = {}
    for c in C:
        d = select_depot_for_client(c, tau_assign, cost_matrix, DEPOTS)
        assign[c] = d
    return assign

def greedy_route_for_depot(d, clientes_d, tij, ei, li):
    """
    Construcción greedy de la ruta para el depósito d
    clientes_d: lista de clientes asignados a este depósito
    tij: matriz de tiempos
    ei, li: ventanas de tiempo
    """
    ruta = [d]
    current = d
    current_time = 0
    
    pendientes = clientes_d.copy()

    while pendientes:
        mejor_j = None
        mejor_incremento = float("inf")
        mejor_arrival = None
        mejor_start_service = None

        for j in pendientes:

            travel = tij[current][j]
            arrival = current_time + travel

            # ventana de tiempo no factible
            if arrival > li[j]:
                continue  # no factible

            # esperar si llegamos antes
            start_service = max(arrival, ei[j])

            # costo incremental según el paper
            incremento = travel

            # elegir el mejor factible
            if incremento < mejor_incremento:
                mejor_incremento = incremento
                mejor_j = j
                mejor_arrival = arrival
                mejor_start_service = start_service

        # si no hay factibles → forzar retorno
        if mejor_j is None:
            break

        # agregar cliente a la ruta
        ruta.append(mejor_j)
        pendientes.remove(mejor_j)

        # actualizar estado
        current = mejor_j
        current_time = mejor_start_service  # service_time = 0

    # retornar al depósito
    ruta.append(RETURNS[d])

    return ruta

# =============================
# ACO principal
# el numero de ants no esta relacionado con la cantidad de vehicilos
# cada hormiga k va a generar una ruta para cada vehivulo v

#Una hormiga = una asignación completa de clientes → vehículos + orden.
#Un vehículo v = una subruta dentro de la solución de la hormiga.

# =============================
mejor_costo_global = float("inf")
mejor_asignacion_global = None
mejor_rutas_global = None

for iteration in range(NUM_ITER):
    solutions = []

    for k in range(NUM_ANTS):
        #FASE 1: Asignacion de customers a depots
        assign = assignment_phase(C, DEPOTS, tau_assign, cost_matrix)
        
        #FASE 2: Greedy para constriccion de rutas respetando restricciones
        rutas = {}
        costo_total = 0

        for idx_d, d in enumerate(DEPOTS):
            clientes_d = [c for c, dep_idx in assign.items() if dep_idx == idx_d]

            if not clientes_d:
                continue

            ruta_d = greedy_route_for_depot(d, clientes_d, tij, ei, li) # No devuelve indices, devuelve numero nodos
            rutas[d] = ruta_d

            # calcular costo de la ruta
            dist = 0
            for a, b in zip(ruta_d[:-1], ruta_d[1:]):
                dist += cost_matrix[a][b]

            costo_total += dist
            costo_total += F[idx_d]  # costo fijo por vehículo

        # Guardar la solución de esta hormiga
        solutions.append((assign, rutas, costo_total))

    # Selección de la mejor hormiga de la iteración
    asign_mejor, rutas_mejor, costo_mejor = min(solutions, key=lambda x: x[2])

    # Actualizar el mejor global si es necesario
    if costo_mejor < mejor_costo_global:
        mejor_costo_global = costo_mejor
        mejor_asignacion_global = asign_mejor
        mejor_rutas_global = rutas_mejor

    
    # FASE 3: Actualización de feromonas
    # evaporación
    tau_assign *= (1 - RHO)

    # refuerzo de la mejor hormiga
    for c in C:
        d = asign_mejor[c]
        tau_assign[d][c] += Q / costo_mejor

print("\n========================")
print("   MEJOR SOLUCIÓN ACO   ")
print("========================")

print(f"Costo total: {mejor_costo_global:.2f}\n")

print("Rutas por depósito:")
for d in DEPOTS:
    if d in mejor_rutas_global:
        ruta = mejor_rutas_global[d]
        print(f"  Depósito {d}: {ruta}")
    else:
        print(f"  Depósito {d}: (vehículo no usado)")
