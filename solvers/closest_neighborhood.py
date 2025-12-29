import numpy as np

# =============================
# BASELINE: Closest Neighbor VRP-TW
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

# -----------------------------
# FASE 1: Asignación simple
# -----------------------------
# assign[c] = índice lógico del vehículo
assign = {}
for c in C:
    best_v = None
    best_cost = float("inf")

    for v in range(V):
        d_node = DEPOTS[v]
        if cost_matrix[d_node][c] < best_cost:
            best_cost = cost_matrix[d_node][c]
            best_v = v

    assign[c] = best_v

# -----------------------------
# FASE 2: Ruteo greedy por vehículo
# -----------------------------
def baseline_md_vrp_tw():
    rutas = {}
    costo_total = 0

    for v in range(V):
        depot = DEPOTS[v]
        ret = RETURNS[depot]

        clientes_v = [c for c, vv in assign.items() if vv == v]
        if not clientes_v:
            continue

        ruta = [depot]
        tiempo_actual = 0
        nodo_actual = depot
        no_visitados = set(clientes_v)

        while no_visitados:
            candidatos = []

            for c in no_visitados:
                travel_time = tij[nodo_actual][c]
                llegada = tiempo_actual + travel_time
                inicio_servicio = max(llegada, ei[c])

                if inicio_servicio <= li[c]:
                    candidatos.append((c, travel_time, inicio_servicio))

            if not candidatos:
                # No se pueden atender todos los clientes asignados
                return None, float("inf"), no_visitados

            # elegir el más cercano (menor tiempo de viaje)
            c_next, travel_time, inicio_servicio = min(
                candidatos, key=lambda x: x[1]
            )

            ruta.append(c_next)
            tiempo_actual = inicio_servicio
            nodo_actual = c_next
            no_visitados.remove(c_next)

        # cerrar ruta en el return
        ruta.append(ret)
        rutas[v] = ruta

        # -----------------------------
        # costo de la ruta
        # -----------------------------
        dist = 0
        for a, b in zip(ruta[:-1], ruta[1:]):
            dist += cost_matrix[a][b]

        costo_total += dist
        costo_total += F[v]  # penalización por usar vehículo
    return rutas, costo_total, []

rutas, costo, no_visitados = baseline_md_vrp_tw()
print("\n========================")
print("  SOLUCIÓN BASELINE NN  ")
print("========================")

if rutas is None:
    print("⚠️ Solución INFACTIBLE")
    print("Clientes no atendidos:", no_visitados)
else:
    print(f"Costo total: {costo:.2f}\n")

    print("Rutas por depósito:")
    for v in range(V):
        depot_node = DEPOTS[v]
        if v in rutas:
            print(f"  Depósito {depot_node} (vehículo {v}): {rutas[v]}")
        else:
            print(f"  Depósito {depot_node} (vehículo {v}): (vehículo no usado)")
