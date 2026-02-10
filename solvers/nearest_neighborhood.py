"""
BASELINE: Nearest Neighbor VRP-TW
"""
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from models.solutions import Solution

class NearestNeighborSolver(BaseSolver):
    def __init__(self):
        pass

    # def phase_one(self, instance: ProblemInstance) -> dict:
    #     """
    #     FASE 1: Asignación simple
    #     """
    #     assign = {}
    #     for c in instance.C:
    #         best_v = None
    #         best_cost = float("inf")

    #         for v in range(instance.V):
    #             d_node = instance.DEPOTS[v]
    #             if instance.cost_matrix[d_node][c] < best_cost:
    #                 best_cost = instance.cost_matrix[d_node][c]
    #                 best_v = v

    #         assign[c] = best_v
    #     return assign

    def phase_one(self, instance):
        """
        Asignación cliente → vehículo respetando ventanas de tiempo.
        NO construye rutas finales.
        Asignacion factible anticipada
        """

        V = instance.V
        C = instance.C
        Q = instance.Q.copy()

        # ordenar clientes por urgencia temporal
        clientes = sorted(
            C,
            key=lambda c: (instance.ei[c] + instance.li[c]) / 2
        )

        # estado por vehículo
        current_node = {instance.DEPOTS[v]: instance.DEPOTS[v] for v in range(V)}
        current_time = {v: 0 for v in range(V)}

        assign = {}
        unsolved_clients = []

        for c in clientes:

            best_v = None
            best_time = float("inf")

            for v in range(V):
                if Q[v] == 0:
                    break
                u = current_node[instance.DEPOTS[v]]

                travel = instance.tij[u][c]
                arrival = current_time[v] + travel
                start_service = max(arrival, instance.ei[c])

                if start_service <= instance.li[c]:
                    if start_service < best_time:
                        best_time = start_service
                        best_v = v

            if best_v is None:
                unsolved_clients.append(c)
            else:
                assign[c] = best_v
                current_node[best_v] = c
                current_time[best_v] = best_time + instance.service_time[c]
                Q[v] -= 1
                
        return assign, unsolved_clients

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

            travel_back = instance.tij[nodo_actual][ret]
            llegada_return = tiempo_actual + travel_back

            if llegada_return > instance.li[ret]:
                return None, float("inf"), no_visitados

            # cerrar ruta en el return
            ruta.append(ret)
            rutas[instance.DEPOTS[v]] = ruta

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
        assign, unsolved_clients = self.phase_one(instance)
        if unsolved_clients:
            return Solution(feasible=False, total_cost=float("inf"), routes={}, unserved_customers=unsolved_clients)
        
        rutas, costo, no_visitados = self.phase_two(instance, assign)
        return Solution(routes=rutas, total_cost=costo, feasible=len(no_visitados)==0,unserved_customers=no_visitados)

    def is_stochastic(self) -> bool:
        return True

    def get_solver_name(self) -> str:
        return "NearestNeighbor"
