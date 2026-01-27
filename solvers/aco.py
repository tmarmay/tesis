"""
aco.py
Solver Ant Colony System for MD-VRP-TW.
3.c.1 version.
"""
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from models.solutions import Solution

import random
import numpy as np 


class ACOSolver(BaseSolver):

    def __init__(self):
        self.NUM_ANTS = 100
        self.NUM_ITER = 1000
        self.ALPHA = 1.0       # influencia de la feromona
        self.BETA = 5.0        # influencia de la heurística (1/distancia)
        self.RHO = 0.5         # tasa de evaporación
        self.PHE = 100           # cantidad de feromona depositada
        self.LAMBDA = 5
        self.penalty = 10
        self.TAU_MAX = 10
        self.TAU_MIN = 1e-4

    def phase_one(self, instance: ProblemInstance) -> dict:
        # =============================
        # Inicialización de feromonas
        # =============================
        tau_assign = np.ones((instance.V, instance.CUSTOMERS)) # Feromonas a los clientes
        best_route = None
        best_cost = float("inf") #Tiene que evaluar igual que objective_rule de milp 
        tau_assign = np.clip(tau_assign, self.TAU_MIN, self.TAU_MAX)
        return tau_assign, best_route, best_cost

    def select_depot_for_client(self, c, tau_assign, cost_matrix, depot_nodes):
        numeradores = []
        for d_idx, d_node in enumerate(depot_nodes):

            tau_dc = tau_assign[d_idx][c] ** self.ALPHA
            eta_dc = (1 / cost_matrix[d_node][c]) ** self.BETA

            numeradores.append(tau_dc * eta_dc)

        total = sum(numeradores)
        if total == 0:
            return random.choice(range(len(depot_nodes)))

        probs = [n / total for n in numeradores]

        # devolvés el índice del depósito
        return random.choices(range(len(depot_nodes)), weights=probs, k=1)[0]

    def assignment_phase(self, C, DEPOTS, tau_assign, cost_matrix) -> dict:
        assign = {}
        for c in C:
            d = self.select_depot_for_client(c, tau_assign, cost_matrix, DEPOTS)
            assign[c] = d
        return assign

    def greedy_route_for_depot(self, d, clientes_d, tij, ei, li, RETURNS) -> tuple:
        """
        Construcción greedy de la ruta para el depósito d
        clientes_d: lista de clientes asignados a este depósito
        tij: matriz de tiempos
        ei, li: ventanas de tiempo
        """
        ruta = [d]
        current = d
        current_time = 0
        unsolved_clients = []
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
                    unsolved_clients.append(j)
                    continue

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
        return ruta, unsolved_clients

    def aco(self, instance: ProblemInstance):
        # =============================
        # ACO principal
        # el numero de ants no esta relacionado con la cantidad de vehicilos
        # cada hormiga k va a generar una ruta para cada vehivulo v

        #Una hormiga = una asignación completa de clientes → vehículos + orden.
        #Un vehículo v = una subruta dentro de la solución de la hormiga.

        # =============================
        tau_assign, best_route, best_cost = self.phase_one(instance)
        mejor_costo_global = float("inf")
        mejor_asignacion_global = None
        mejor_rutas_global = None

        for iteration in range(self.NUM_ITER):
            solutions = []

            for k in range(self.NUM_ANTS):
                unsolved_total = []

                #FASE 1: Asignacion de customers a depots
                assign = self.assignment_phase(instance.C, instance.DEPOTS, tau_assign, instance.cost_matrix)
                
                #FASE 2: Greedy para constriccion de rutas respetando restricciones
                rutas = {}
                costo_total = 0

                for idx_d, d in enumerate(instance.DEPOTS):
                    clientes_d = [c for c, dep_idx in assign.items() if dep_idx == idx_d]
                    if not clientes_d:
                        continue

                    ruta_d, unsolved_clientes = self.greedy_route_for_depot(d, clientes_d, instance.tij, instance.ei, instance.li, instance.RETURNS) # No devuelve indices, devuelve numero nodos
                    unsolved_total.extend(unsolved_clientes)
                    rutas[d] = ruta_d

                    # calcular costo de la ruta
                    dist = 0
                    for a, b in zip(ruta_d[:-1], ruta_d[1:]):
                        dist += instance.cost_matrix[a][b]

                    costo_total += dist
                    costo_total += instance.F[idx_d]  # costo fijo por vehículo

                # Guardar la solución de esta hormiga
                solutions.append((assign, rutas, costo_total, unsolved_total))

            # Selección de la mejor hormiga de la iteración
            asign_mejor, rutas_mejor, costo_mejor, unsolved_clientes = min(
                solutions,
                key=lambda x: (len(x[3]), x[2])   # primero factibilidad, luego costo
            )

            # Actualizar el mejor global si es necesario
            if costo_mejor < mejor_costo_global and len(unsolved_clientes) == 0:
                mejor_costo_global = costo_mejor
                mejor_asignacion_global = asign_mejor
                mejor_rutas_global = rutas_mejor

            
            # FASE 3: Actualización de feromonas
            # Evaporación
            tau_assign *= (1 - self.RHO)

            # Definir delta según factibilidad
            if len(unsolved_clientes) == 0:
                delta = self.PHE / costo_mejor
            else:
                delta = self.PHE / (costo_mejor + self.LAMBDA * len(unsolved_clientes))

            # Refuerzo SOLO de la mejor hormiga
            for c in instance.C:
                d = asign_mejor[c]
                tau_assign[d][c] += delta

            return mejor_rutas_global, mejor_costo_global, unsolved_clientes
                
    def solve(self, instance: ProblemInstance):
        rutas, costo, no_visitados = self.aco(instance)
        return Solution(routes=rutas, total_cost=costo, feasible=len(no_visitados)==0,unserved_customers=no_visitados)
