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
V = 1 # Vehicles = Depots
CUSTOMERS = 2
N = CUSTOMERS + V # por el momento con el mismo depot y return

C = [i for i in range(CUSTOMERS)] #CUSTOMERS
DEPOTS = [i for i in range(C[-1] + 1, C[-1] + 1 + V)]
RETURNS = DEPOTS # SOLO PORQUE ESTOY EN EL MODELO SIMPLIDICADO

cost_matrix = np.array([[100,1,12],
                        [1,100,8], #la matriz tiene que ser espejo con la diagonal porque no es dirigido
                        [12,8,100]]) # para decir que no puedo ir de i a j: Poner 0 en eta[i][j] y/o tau[i][j] va a hacer que la prob sea 0

F = [5 for _ in range(V)] # penalizacion por usar auto
# =============================
# Inicialización de feromonas
# =============================
tau = np.ones((N, N)) # Misma dim que c_ij
best_route = None
best_cost = float("inf") #Tiene que evaluar igual que objective_rule de milp 

# =============================
# Función: elegir próximo nodo
# Devuelve el indice del proximo nodo
# =============================
def select_next_node(current: int, unvisited: list) -> int:
    probs = []
    total = 0.0
    for j in unvisited:
        tau_ij = tau[current][j] ** ALPHA
        eta_ij = (1 / cost_matrix[current][j]) ** BETA
        probs.append(tau_ij * eta_ij)
        total += probs[-1]

    if total == 0:
        # fallback: elegir aleatorio
        return random.choice(list(unvisited))

    probs = [p / total for p in probs]
    return random.choices(list(unvisited), weights=probs, k=1)[0]

# =============================
# ACO principal
# el numero de ants no esta relacionado con la cantidad de vehicilos
# cada hormiga k va a generar unba rura para cada vehivulo v

#Una hormiga = una asignación completa de clientes → vehículos + orden.
#Un vehículo v = una subruta dentro de la solución de la hormiga.

# =============================
for iteration in range(NUM_ITER):
    solutions = []

    for k in range(NUM_ANTS):
        route = []
        total_distance = 0 # agregar total cost tamb usando la funcion

        for v in DEPOTS:
            # cada hormiga empieza en el depósito 0
            route = [v] #modificar para cada una salga de su depot
            unvisited = set(C) - set(route) # clientes sin visitar
            current = route[-1]
            ready2return = 'exploring'
            
            while unvisited:
                next_node = select_next_node(current, unvisited)
                total_distance += cost_matrix[current][next_node]
                route.append(next_node)
                unvisited.remove(next_node)
                current = next_node

                if not unvisited and ready2return != 'returing':
                    ready2return = 'returing'
                    unvisited.add(RETURNS[0])
            # volver al depósito
            #total_distance += cost_matrix[current][RETURNS[0]] #deberia ser [RETURNS[current]]
            #route.append(RETURNS[0]) #igual aca
            solutions.append((route, total_distance))

            # penalización por usar este vehículo
            if len(route) > 2:
                total_distance += F[V - v]

    # Mejor de la iteración de la ant k
    iteration_best = min(solutions, key=lambda x: x[1])
    if iteration_best[1] < best_cost:
        best_route, best_cost = iteration_best

    # Evaporación
    tau *= (1 - RHO)

    # Reforzar arcos de la mejor hormiga de la iteración
    for i in range(len(iteration_best[0]) - 1):
        a, b = iteration_best[0][i], iteration_best[0][i + 1]
        tau[a][b] += Q / iteration_best[1]

    if iteration % 10 == 0:
        print(f"Iteración {iteration}: mejor costo = {best_cost:.2f}")

# =============================
# Resultado final
# =============================
print("\n=== Mejor solución encontrada ===")
print("Ruta:", best_route)
print("Costo total:", round(best_cost, 2))

