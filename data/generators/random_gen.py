import math
import numpy as np
from models.problem_instance import ProblemInstance


class RandomGenerator:
    """
    Generador aleatorio de instancias MD-VRP-TW.

    A diferencia de SyntheticGenerator, no construye una solución factible
    previa para derivar T_MAX ni para centrar las ventanas de tiempo.
    Las instancias generadas pueden ser infactibles; la validación se reporta
    pero no lanza errores.
    """

    def __init__(self, *, cfg_experiment: dict, cfg_generator: dict):
        cost_range = cfg_generator['cost_range']
        cost_ranges = cfg_generator['matrix_costs_ranges']
        tw_tightness = cfg_generator['tw_tightness']
        time_windows_tightness = cfg_generator['time_windows_tightness']

        self.num_customers = cfg_experiment['num_customers']
        self.num_vehicles = cfg_experiment['num_vehicles']
        self.capacity = list(cfg_experiment['capacity']) * self.num_vehicles
        self.vehicle_penalty = cfg_experiment['vehicle_penalty']
        self.customer_demand = cfg_experiment['customer_demand']
        self.cost_low, self.cost_high = cost_ranges[cost_range]
        self.tw_low, self.tw_high = time_windows_tightness[tw_tightness]
        self.tw_min_value, self.tw_max_value = cfg_generator['time_windows_values']
        self.tmax_factor = cfg_generator.get('tmax_factor', 1.5)
        self.seed = cfg_experiment['seed']
        self.T_MAX = np.inf

        self.rng = np.random.default_rng(self.seed)

    def _compute_tmax(self, tij) -> int:
        """
        T_MAX heurístico basado en estadísticas de tij, sin construir rutas.
        Escala con la longitud media de una ruta típica y el tiempo de viaje medio.
        """
        mean_hop = float(tij.mean())
        avg_hops = max(2, self.num_customers // self.num_vehicles + 2)
        return int(mean_hop * avg_hops * self.tmax_factor) + 1

    def _generate_random_time_windows(self, tij) -> tuple[list, list]:
        TW_DIM = self.num_customers + 2 * self.num_vehicles
        C = list(range(self.num_customers))
        DEPOTS = list(range(C[-1] + 1, C[-1] + 1 + self.num_vehicles))
        RETURNS = list(range(C[-1] + self.num_vehicles + 1, TW_DIM))

        self.T_MAX = self._compute_tmax(tij)

        ei = [0] * TW_DIM
        li = [self.T_MAX] * TW_DIM

        tw_range = max(1, self.tw_high - self.tw_low)
        for c in C:
            # C6: ei[c] debe permitir al menos un retorno posible
            min_return_hop = min(int(tij[c][r]) for r in RETURNS)
            max_ei = max(0, self.T_MAX - min_return_hop)

            width = int(self.rng.integers(0, tw_range + 1)) + self.tw_low
            start = int(self.rng.integers(0, max(1, max_ei + 1)))
            ei[c] = min(start, max_ei)
            li[c] = min(self.T_MAX, ei[c] + width)

            # C5: li[c] debe ser alcanzable desde al menos un depot
            min_depot_hop = min(int(tij[d][c]) for d in DEPOTS)
            if li[c] < min_depot_hop:
                li[c] = min(self.T_MAX, min_depot_hop + 1)

            if li[c] <= ei[c]:
                li[c] = ei[c] + 1

        for d in DEPOTS + RETURNS:
            ei[d] = 0
            li[d] = self.T_MAX

        return ei, li

    def generate(self) -> ProblemInstance:
        n = self.num_customers
        V = self.num_vehicles
        N = n + 2 * V

        M = self.rng.integers(self.cost_low, self.cost_high, size=(N, N))
        cost_matrix = (M + M.T) // 2
        np.fill_diagonal(cost_matrix, 99)

        tij = self.rng.integers(5, 10, size=(N, N))

        ei, li = self._generate_random_time_windows(tij)

        pi = ProblemInstance(
            name=f"random_n{n}_v{V}_seed{self.seed}",
            V=V,
            CUSTOMERS=n,
            cost_matrix=cost_matrix,
            tij=tij,
            ei=ei,
            li=li,
            F=[self.vehicle_penalty for _ in range(V)],
            demands=[1 for _ in range(n)],
            Q=self.capacity,
            reference_cost=None,
        )
        self._validate_instance(instance=pi, verbose=True)
        return pi

    def _validate_instance(self, instance: ProblemInstance, verbose: bool = True) -> bool:
        errors = []
        warnings = []

        tij = instance.tij
        ei = instance.ei
        li = instance.li
        C = instance.C
        DEPOTS = instance.DEPOTS
        RETURNS = instance.RETURNS_milp
        V = instance.V
        Q = instance.Q
        demands = instance.demands
        N = instance.N
        T_MAX = max(li)

        total_demand = sum(demands)
        total_capacity = sum(Q)
        if total_demand > total_capacity:
            errors.append(
                f"[C1] INFACTIBLE: demanda total ({total_demand}) > "
                f"capacidad total de la flota ({total_capacity})."
            )
        elif verbose:
            print(f"[C1] OK — demanda total={total_demand}, capacidad flota={total_capacity}.")

        max_q = max(Q)
        if any(d > max_q for d in demands):
            bad = [i for i, d in enumerate(demands) if d > max_q]
            errors.append(
                f"[C2] INFACTIBLE: clientes {bad} tienen demanda > capacidad máxima "
                f"de cualquier vehículo ({max_q})."
            )
        elif verbose:
            print(f"[C2] OK — demanda por cliente={set(demands)}, Q_max={max_q}.")

        degenerate = [i for i in range(N) if ei[i] >= li[i]]
        if degenerate:
            errors.append(
                f"[C3] INFACTIBLE: nodos {degenerate} tienen ei >= li."
            )
        elif verbose:
            print(f"[C3] OK — todas las ventanas tienen ei < li.")

        over_tmax = [i for i in range(N) if li[i] > T_MAX]
        if over_tmax:
            warnings.append(
                f"[C4] ADVERTENCIA: nodos {over_tmax} tienen li > T_MAX={T_MAX}."
            )
        elif verbose:
            print(f"[C4] OK — todos li <= T_MAX={T_MAX}.")

        unreachable = []
        for c in C:
            if not any(ei[d] + tij[d][c] <= li[c] for d in DEPOTS):
                unreachable.append(c)
        if unreachable:
            errors.append(
                f"[C5] INFACTIBLE: clientes {unreachable} no son alcanzables "
                f"desde ningún depot dentro de su ventana."
            )
        elif verbose:
            print(f"[C5] OK — todos los clientes son alcanzables desde al menos un depot.")

        no_return = []
        for c in C:
            if not any(ei[c] + tij[c][r] <= li[r] for r in RETURNS):
                no_return.append(c)
        if no_return:
            errors.append(
                f"[C6] INFACTIBLE: clientes {no_return} no pueden regresar "
                f"a ningún nodo de retorno dentro de su ventana."
            )
        elif verbose:
            print(f"[C6] OK — todos los clientes pueden retornar a algún nodo de retorno.")

        total_pairs = len(C) * (len(C) - 1)
        reachable_pairs = sum(
            1 for i in C for j in C if i != j and ei[i] + tij[i][j] <= li[j]
        )
        if total_pairs > 0:
            frac = reachable_pairs / total_pairs
            msg = (
                f"[C7] Pares cliente-cliente alcanzables en tiempo: "
                f"{reachable_pairs}/{total_pairs} ({frac:.1%})."
            )
            if frac < 0.1:
                warnings.append(msg + " — MUY POCOS pares alcanzables.")
            elif verbose:
                print(msg)

        min_vehicles_needed = math.ceil(total_demand / max_q)
        if min_vehicles_needed > V:
            errors.append(
                f"[C8] INFACTIBLE: se necesitan al menos {min_vehicles_needed} vehículos "
                f"pero solo hay {V}."
            )
        elif verbose:
            print(f"[C8] OK — vehículos disponibles={V}, mínimo necesario={min_vehicles_needed}.")

        print()
        for w in warnings:
            print(f"  ⚠  {w}")
        if errors:
            for e in errors:
                print(f"  ✗  {e}")
            print(f"\n  → Instancia '{instance.name}': POTENCIALMENTE INFACTIBLE "
                  f"({len(errors)} error(es) encontrado(s)).\n")
            return False
        print(f"  ✓  Instancia '{instance.name}': pasa todas las verificaciones.\n")
        return True

    def __str__(self) -> str:
        lines = [
            "RandomGenerator",
            "-" * 15,
            f"Vehicles: {self.num_vehicles}",
            f"Customers: {self.num_customers}",
            f"Total nodes: {self.num_customers + 2 * self.num_vehicles}",
            "",
            "Cost matrix:",
            f"  range: [{self.cost_low}, {self.cost_high}]",
            "  symmetric: True",
            "",
            "Time windows:",
            f"  T_MAX: {self.T_MAX}",
            f"  width range: [{self.tw_low}, {self.tw_high}]",
            f"  tmax_factor: {self.tmax_factor}",
            "",
            "Vehicle capacity:",
            f"  Q per vehicle: {self.capacity}",
            f"Random seed: {self.seed}",
        ]
        return "\n".join(lines)
