"""
aco_v2.py
Solver ACO for MD-VRP-TW.
Changes vs v1:
- greedy_route_for_depot uses combined criterion: travel + W_URGENCY * start_service
Changes vs v1 (routing pheromones):
- tau_route[i][j] pheromone matrix on client->client arcs
- stochastic ACS selection in routing phase (exploit with Q0, explore otherwise)
- combined criterion becomes eta heuristic: 1 / (travel + W_URGENCY * start_service)
"""
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from models.solutions import Solution

import random
import time
import numpy as np



class ACOSolverV2(BaseSolver):
    def __init__(self, cfg_aco: dict=None):
        if cfg_aco is None:
            self.NUM_ANTS = 100
            self.NUM_ITER = 1000
            self.ALPHA = 1.0
            self.BETA = 5.0
            self.RHO = 0.5
            self.PHE = 100
            self.GAMMA = 2
            self.LAMBDA = 5
            self.penalty = 10
            self.TAU_MAX = 10
            self.TAU_MIN = 1e-4
            self.W_URGENCY = 0.4
            self.Q0 = 0.9
        else:
            self.NUM_ANTS = cfg_aco['num_ants']
            self.NUM_ITER = cfg_aco['num_iter']
            self.ALPHA = cfg_aco['alpha']
            self.BETA = cfg_aco['beta']
            self.RHO = cfg_aco['rho']
            self.PHE = cfg_aco['phe']
            self.GAMMA = cfg_aco['gamma']
            self.LAMBDA = cfg_aco['lambda']
            self.penalty = cfg_aco['penalty']
            self.TAU_MAX = cfg_aco['tau_max']
            self.TAU_MIN = cfg_aco['tau_min']
            self.W_URGENCY = cfg_aco['w_urgency']
            self.Q0 = cfg_aco['q0']

    def phase_one(self, instance: ProblemInstance) -> dict:
        tau_assign = np.ones((instance.V, instance.CUSTOMERS))
        tau_assign = np.clip(tau_assign, self.TAU_MIN, self.TAU_MAX)

        N = instance.tij.shape[0]
        tau_route = np.full((N, N), self.TAU_MIN)

        return tau_assign, tau_route

    def select_depot_for_client(self, c, tau_assign, cost_matrix, depot_nodes, Q_initial, Q_current):
        numeradores = []
        for d_idx, d_node in enumerate(depot_nodes):
            tau_dc = tau_assign[d_idx][c] ** self.ALPHA
            eta_dc = (1 / cost_matrix[d_node][c]) ** self.BETA
            numeradores.append(tau_dc * eta_dc)

        total = sum(numeradores)
        if total == 0:
            return random.choice(range(len(depot_nodes)))

        probs = [n / total for n in numeradores]
        return random.choices(range(len(depot_nodes)), weights=probs, k=1)[0]

    def assignment_phase(self, C, DEPOTS, tau_assign, cost_matrix, Q_initial, Q_current) -> dict:
        assign = {}
        for c in C:
            d = self.select_depot_for_client(c, tau_assign, cost_matrix, DEPOTS, Q_initial, Q_current)
            assign[c] = d
        return assign

    def greedy_route_for_depot(self, idx_d, d, clientes_d, tij, ei, li, RETURNS, Q, tau_route, cost_matrix) -> tuple:
        """
        Construye la ruta para el depósito d usando selección ACS sobre arcos cliente->cliente.
        value = tau^alpha * eta^beta * mu^gamma
        eta_ij = 1 / (travel + W_URGENCY * start_service)
        mu_ij  = Clarke-Wright savings: cost[current][depot] + cost[depot][j] - cost[current][j]
        Con prob Q0 explota (argmax), sino exploración por ruleta.
        """
        ruta = [d]
        current = d
        current_time = 0
        unsolved_clients = []
        pendientes = clientes_d.copy()

        while pendientes:
            if Q[idx_d] <= 0:
                unsolved_clients.extend(pendientes)
                break

            candidatos = []
            for j in pendientes:
                travel = tij[current][j]
                arrival = current_time + travel

                if arrival > li[j]:
                    continue

                start_service = max(arrival, ei[j])
                score = travel + self.W_URGENCY * start_service
                eta = (1.0 / score) ** self.BETA
                tau = tau_route[current][j] ** self.ALPHA
                savings = cost_matrix[current][d] + cost_matrix[d][j] - cost_matrix[current][j]
                mu = max(savings, 0.0) + 1.0  # +1 para evitar cero (neutro cuando savings <= 0)
                candidatos.append((j, start_service, tau * eta * (mu ** self.GAMMA)))

            if not candidatos:
                unsolved_clients.extend(pendientes)
                break

            if random.random() < self.Q0:
                mejor_j, mejor_start_service, _ = max(candidatos, key=lambda x: x[2])
            else:
                valores = [c[2] for c in candidatos]
                total = sum(valores)
                if total == 0:
                    mejor_j, mejor_start_service, _ = random.choice(candidatos)
                else:
                    probs = [v / total for v in valores]
                    mejor_j, mejor_start_service, _ = random.choices(candidatos, weights=probs, k=1)[0]

            ruta.append(mejor_j)
            pendientes.remove(mejor_j)
            Q[idx_d] -= 1
            current = mejor_j
            current_time = mejor_start_service

        ruta.append(RETURNS[d])
        return ruta, unsolved_clients

    def _is_tw_feasible(self, ruta, instance) -> bool:
        current_time = instance.ei[ruta[0]]
        for i, j in zip(ruta[:-1], ruta[1:]):
            arrival = current_time + instance.tij[i][j]
            if arrival > instance.li[j]:
                return False
            current_time = max(arrival, instance.ei[j])
        return True

    def _insert_orphan(self, c, rutas, instance) -> tuple:
        best_depot, best_pos, best_delta = None, None, float('inf')
        for depot, ruta in rutas.items():
            for i in range(1, len(ruta)):
                nueva = ruta[:i] + [c] + ruta[i:]
                if not self._is_tw_feasible(nueva, instance):
                    continue
                delta = (instance.cost_matrix[ruta[i-1]][c] +
                         instance.cost_matrix[c][ruta[i]] -
                         instance.cost_matrix[ruta[i-1]][ruta[i]])
                if delta < best_delta:
                    best_depot, best_pos, best_delta = depot, i, delta
        return best_depot, best_pos

    def eliminate_vehicles(self, rutas, instance) -> dict:
        mejor = {d: r[:] for d, r in rutas.items()}
        mejor_costo = sum(
            instance.cost_matrix[a][b]
            for ruta in mejor.values()
            for a, b in zip(ruta[:-1], ruta[1:])
        )
        improved = True
        while improved:
            improved = False
            for depot in list(mejor.keys()):
                huerfanos = sorted(
                    mejor[depot][1:-1],
                    key=lambda c: instance.li[c] - instance.ei[c]
                )
                restantes = {d: r[:] for d, r in mejor.items() if d != depot}

                factible = True
                for c in huerfanos:
                    dep, pos = self._insert_orphan(c, restantes, instance)
                    if dep is None:
                        factible = False
                        break
                    restantes[dep] = restantes[dep][:pos] + [c] + restantes[dep][pos:]

                if not factible:
                    continue

                nuevo_costo = sum(
                    instance.cost_matrix[a][b]
                    for ruta in restantes.values()
                    for a, b in zip(ruta[:-1], ruta[1:])
                )
                if nuevo_costo <= mejor_costo:
                    mejor = restantes
                    mejor_costo = nuevo_costo
                    improved = True
                    break

        return mejor

    def two_opt(self, ruta, instance) -> list:
        best = ruta[:]
        best_cost = sum(instance.cost_matrix[a][b] for a, b in zip(best[:-1], best[1:]))
        improved = True

        while improved:
            improved = False
            for i in range(1, len(best) - 2):
                for j in range(i + 1, len(best) - 1):
                    candidate = best[:i] + best[i:j+1][::-1] + best[j+1:]
                    if not self._is_tw_feasible(candidate, instance):
                        continue
                    candidate_cost = sum(instance.cost_matrix[a][b] for a, b in zip(candidate[:-1], candidate[1:]))
                    if candidate_cost < best_cost:
                        best = candidate
                        best_cost = candidate_cost
                        improved = True
                        break
                if improved:
                    break

        return best

    def aco(self, instance: ProblemInstance):
        tau_assign, tau_route = self.phase_one(instance)
        mejor_costo_global = float("inf")
        mejor_asignacion_global = None
        mejor_rutas_global = None

        #for iteration in range(self.NUM_ITER):
        import time
        start = time.time()
        while time.time() - start < 60:
            solutions = []

            for k in range(self.NUM_ANTS):
                Q = instance.Q.copy()
                DEPOTS = instance.DEPOTS.copy()
                unsolved_total = []

                assign = self.assignment_phase(instance.C, DEPOTS, tau_assign, instance.cost_matrix, instance.Q, Q)

                rutas = {}
                costo_total = 0

                for idx_d, d in enumerate(instance.DEPOTS):
                    clientes_d = [c for c, dep_idx in assign.items() if dep_idx == idx_d]
                    if not clientes_d:
                        continue

                    ruta_d, unsolved_clientes = self.greedy_route_for_depot(
                        idx_d, d, clientes_d, instance.tij,
                        instance.ei, instance.li,
                        instance.RETURNS, Q, tau_route, instance.cost_matrix
                    )
                    unsolved_total.extend(unsolved_clientes)
                    rutas[d] = ruta_d

                    dist = 0
                    for a, b in zip(ruta_d[:-1], ruta_d[1:]):
                        dist += instance.cost_matrix[a][b]

                    costo_total += dist
                    costo_total += instance.F[idx_d]

                solutions.append((assign, rutas, costo_total, unsolved_total))

            asign_mejor, rutas_mejor, costo_mejor, unsolved_clientes = min(
                solutions,
                key=lambda x: (len(x[3]), x[2])
            )

            if costo_mejor < mejor_costo_global and len(unsolved_clientes) == 0:
                mejor_costo_global = costo_mejor
                mejor_asignacion_global = asign_mejor
                mejor_rutas_global = rutas_mejor

            # evaporación
            tau_assign *= (1 - self.RHO)
            tau_route *= (1 - self.RHO)

            if len(unsolved_clientes) == 0:
                delta = self.PHE / costo_mejor
            else:
                delta = self.PHE / (costo_mejor + self.LAMBDA * len(unsolved_clientes))

            # refuerzo asignación
            for c in instance.C:
                d = asign_mejor[c]
                tau_assign[d][c] += delta

            # refuerzo ruteo
            for ruta_d in rutas_mejor.values():
                for a, b in zip(ruta_d[:-1], ruta_d[1:]):
                    tau_route[a][b] += delta

            tau_assign = np.clip(tau_assign, self.TAU_MIN, self.TAU_MAX)
            tau_route = np.clip(tau_route, self.TAU_MIN, self.TAU_MAX)

        if mejor_rutas_global is not None:
            mejor_rutas_global = self.eliminate_vehicles(mejor_rutas_global, instance)
            for d, ruta in mejor_rutas_global.items():
                mejor_rutas_global[d] = self.two_opt(ruta, instance)
            mejor_costo_global = sum(
                instance.cost_matrix[a][b]
                for ruta in mejor_rutas_global.values()
                for a, b in zip(ruta[:-1], ruta[1:])
            )
            return mejor_rutas_global, mejor_costo_global, []
        return None, float("inf"), unsolved_clientes

    def solve(self, instance: ProblemInstance):
        rutas, costo, no_visitados = self.aco(instance)
        return Solution(routes=rutas, total_cost=costo, feasible=len(no_visitados)==0, unserved_customers=no_visitados)

    def get_run_params(self) -> dict:
        return {"ants": self.NUM_ANTS, "it": self.NUM_ITER}

    def is_stochastic(self) -> bool:
        return True

    def get_solver_name(self) -> str:
        return "ACO_v2"
