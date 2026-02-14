import numpy as np
from models.problem_instance import ProblemInstance

class SyntheticGenerator:
    def __init__(self, *, cfg_experiment: dict, cfg_generator: dict):
        
        cost_range=cfg_generator['cost_range'] 
        cost_ranges=cfg_generator['matrix_costs_ranges']
        tw_tightness=cfg_generator['tw_tightness']
        time_windows_tightness=cfg_generator['time_windows_tightness']
        self.num_customers = cfg_experiment['num_customers']
        self.num_vehicles = cfg_experiment['num_vehicles']
        self.capacity = list(cfg_experiment['capacity']) * self.num_vehicles
        self.vehicle_penalty = cfg_experiment['vehicle_penalty']
        self.customer_demand = cfg_experiment['customer_demand']
        self.cost_low, self.cost_high = cost_ranges[cost_range]
        self.tw_low, self.tw_high = time_windows_tightness[tw_tightness] #Representa el ancho de las ventanas; no el inicio/fin
        self.tw_min_value, self.tw_max_value = cfg_experiment['time_windows_values']
        self.seed = cfg_experiment['seed']

        self.rng = np.random.default_rng(self.seed)
        
    def _generate_tmax(self, tij) -> None:
        # Largo temporal en el que se desarolla la simulacion
        avg_row_sum = np.mean(np.sum(tij, axis=1))
        self.T_MAX = avg_row_sum

    def _generate_feasible_time_windows(self, DEPOTS, RETURNS, tij) -> tuple[list,list]:
        """
        Genera ventanas garantizando al menos una solución factible.
        Usa construcción greedy por capacidad.
        """
        TW_DIM = self.num_customers + 2 * self.num_vehicles

        ei = [0] * TW_DIM
        li = [self.T_MAX] * TW_DIM

        routes = [[] for _ in range(self.num_vehicles)]
        remaining_capacity = self.capacity.copy()

        customers = [i for i in range(self.num_customers)]
        self.rng.shuffle(customers)

        # Asignacion de rutas
        v = 0
        for c in customers:
            demand = self.customer_demand

            while v < self.num_vehicles and remaining_capacity[v] < demand:
                v += 1

            if v == self.num_vehicles:
                raise ValueError("Instancia base infactible por capacidad.")

            routes[v].append(c)
            remaining_capacity[v] -= demand

        # Simulacion de recorrido
        arrival_times = {}
        for v in range(self.num_vehicles):
            depot = DEPOTS[v]
            current = depot
            time = 0

            for c in routes[v]:
                travel = tij[current][c]
                time += travel
                arrival_times[c] = time
                #time += service_time

                current = c
            return_node = RETURNS[v]
            time += tij[current][return_node]

        # tightness controlado por rango tw_low/tw_high
        for c in range(self.num_customers):
            arrival = arrival_times[c]
            
            # slack depende de ancho permitido
            base_width = self.rng.integers(self.tw_low, self.tw_high)

            left_slack = self.rng.uniform(0.3, 0.7) * base_width
            right_slack = base_width - left_slack

            ei[c] = max(0, int(arrival - left_slack))
            li[c] = min(self.T_MAX, int(arrival + right_slack))

            if li[c] <= ei[c]:
                li[c] = ei[c] + 5

        for d in DEPOTS + RETURNS:
            ei[d] = 0
            li[d] = self.T_MAX

        return ei, li


    def generate(self) -> ProblemInstance:
        """
        Genera una instancia MD-VRP-TW sintética
        """
        n = self.num_customers
        V = self.num_vehicles

        # nodos: [customers] [depots] [returns]
        N = n + 2 * V

        # matriz de costos / tiempos (simétrica)
        M = self.rng.integers(self.cost_low, self.cost_high, size=(N, N))
        cost_matrix = (M + M.T) // 2
        np.fill_diagonal(cost_matrix, 99)

        tij = self.rng.integers(5, 10, size=(N, N))
        self._generate_tmax(tij=tij)

        ei, li = self._generate_feasible_time_windows()

        return ProblemInstance(
            name=f"synthetic_n{n}_v{V}_seed{self.seed}",
            V=V,
            CUSTOMERS=n,
            cost_matrix=cost_matrix,
            tij=tij,
            ei=ei,
            li=li,
            F=[self.vehicle_penalty for _ in range(V)],
            demands=[self.customer_demand for _ in range(n)],
            Q=self.capacity,
        )

    def __str__(self) -> str:
        lines = []

        lines.append("SyntheticGenerator")
        lines.append("-" * 18)

        lines.append(f"Vehicles: {self.num_vehicles}")
        lines.append(f"Customers: {self.num_customers}")
        lines.append(f"Total nodes: {self.num_customers + 2 * self.num_vehicles}")

        lines.append("")
        lines.append("Cost matrix:")
        lines.append(f"  range: [{self.cost_low}, {self.cost_high}]")
        lines.append("  symmetric: True")

        lines.append("")
        lines.append("Time windows:")
        lines.append(f"  T_MAX: {self.T_MAX}")
        lines.append(f"  width range: [{self.tw_low}, {self.tw_high}]")

        lines.append("")
        lines.append("Vehicle capacity:")
        lines.append(f"  Q per vehicle: {self.capacity}")

        if hasattr(self, "seed"):
            lines.append("")
            lines.append(f"Random seed: {self.seed}")

        return "\n".join(lines)