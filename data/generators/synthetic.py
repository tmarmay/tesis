import numpy as np
from models.problem_instance import ProblemInstance

class SyntheticGenerator:
    def __init__(self, *, cfg_experiment: dict, cfg_generator: dict):
        
        cost_range=cfg_generator['cost_range'] 
        cost_ranges=cfg_generator['matrix_costs_ranges']
        tw_tightness=cfg_generator['tw_tightness']
        time_windows_tightness=cfg_generator['time_windows_tightness']
        t_max=cfg_generator['t_max']

        self.num_customers = cfg_experiment['num_customers']
        self.num_vehicles = cfg_experiment['num_vehicles']
        self.capacity = cfg_experiment['capacity']
        self.cost_low, self.cost_high = cost_ranges[cost_range]
        self.tw_low, self.tw_high = time_windows_tightness[tw_tightness] #Representa el ancho de las ventanas; no el inicio/fin
        self.seed = cfg_experiment['seed']
        self.rng = np.random.default_rng(self.seed)
        self.T_MAX = t_max * cfg_experiment['num_customers'] # Largo temporal en el que se desarolla la simulacion

    def generate(self) -> ProblemInstance:
        """
        Genera una instancia MD-VRP-TW sintética
        """
        n = self.num_customers
        V = self.num_vehicles

        # nodos: [customers] [depots] [returns]
        CUSTOMERS = list(range(n))               # customers
        DEPOTS = list(range(n, n+V))             # depots
        RETURNS = list(range(n+V, n+2*V))        # returns

        N = V + n + V

        # matriz de costos / tiempos (simétrica)
        M = self.rng.integers(self.cost_low, self.cost_high, size=(N, N))
        cost_matrix = (M + M.T) // 2
        np.fill_diagonal(cost_matrix, 99)

        tij = self.rng.integers(5, 10, size=(N, N))

        # ventanas de tiempo
        ei = [0] * N
        li = [self.T_MAX] * N

        # ventanas SOLO para customers
        for c in range(n):
            t_i = self.rng.integers(0, self.T_MAX)
            w = self.rng.integers(self.tw_low, self.tw_high)

            ei[c] = max(0, t_i - w // 2)
            li[c] = min(self.T_MAX, ei[c] + w)

        # depots y returns sin restricción fuerte
        for d in range(n, N):
            ei[d] = 0
            li[d] = self.T_MAX

        return ProblemInstance(
            name=f"synthetic_n{n}_v{V}_seed{self.seed}",
            V=V,
            CUSTOMERS=n,
            cost_matrix=cost_matrix,
            tij=tij,
            ei=ei,
            li=li,
            F=[5 for _ in range(V)],
            demands=[1 for _ in range(n)],
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