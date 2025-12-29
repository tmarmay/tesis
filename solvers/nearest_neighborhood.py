"""
BASELINE: Nearest Neighbor VRP-TW
"""
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from models.solutions import Solution

class NearestNeighborSolver(BaseSolver):
    def __init__(self):
        pass

    def phase_one(self, instance: ProblemInstance) -> dict:
        """
        FASE 1: Asignación simple
        """
        assign = {}
        for c in instance.C:
            best_v = None
            best_cost = float("inf")

            for v in range(instance.V):
                d_node = instance.DEPOTS[v]
                if instance.cost_matrix[d_node][c] < best_cost:
                    best_cost = instance.cost_matrix[d_node][c]
                    best_v = v

            assign[c] = best_v
        return assign

    def phase_two(self, instance: ProblemInstance, assign: dict) -> tuple:
        rutas = {}
        costo_total = 0

        for v in range(instance.V):
            depot = instance.DEPOTS[v]
            ret = instance.RETURNS[depot]

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
                    travel_time = instance.tij[nodo_actual][c]
                    llegada = tiempo_actual + travel_time
                    inicio_servicio = max(llegada, instance.ei[c])

                    if inicio_servicio <= instance.li[c]:
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
                dist += instance.cost_matrix[a][b]

            costo_total += dist
            costo_total += instance.F[v]  # penalización por usar vehículo
        return rutas, costo_total, []
    
    def solve(self, instance):
        assign = self.phase_one(instance)
        rutas, costo, no_visitados = self.phase_two(instance, assign)
        return Solution(routes=rutas, total_cost=costo, feasible=len(no_visitados)==0,unserved_customers=no_visitados)

    # def print(self):
    ## no deberia ir pero lo dejo por ahora
    #     print("\n========================")
    #     print("  SOLUCIÓN BASELINE NN  ")
    #     print("========================")

    #     if self.rutas is None:
    #         print("⚠️ Solución INFACTIBLE")
    #         print("Clientes no atendidos:", self.no_visitados)
    #     else:
    #         print(f"Costo total: {self.costo_total:.2f}\n")

    #         print("Rutas por depósito:")
    #         for v in range(V):
    #             depot_node = DEPOTS[v]
    #             if v in self.rutas:
    #                 print(f"  Depósito {depot_node} (vehículo {v}): {self.rutas[v]}")
    #             else:
    #                 print(f"  Depósito {depot_node} (vehículo {v}): (vehículo no usado)")
