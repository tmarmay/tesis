import numpy as np
from models.problem_instance import ProblemInstance

COST_RANGES = [
    (1, 20),    # costos bajos
    (100, 200), # valores altos
    (1, 300),   # alta dispersión
]

# Representa el ancho de las ventanas; no el inicio/fin
TIME_WINDOW_TIGHTNESS = {
    "loose":  (0, 80),
    "medium": (0, 40),
    "tight":  (0, 20),
    "critical": (0, 7),
}

class SyntheticGenerator:
    def __init__(self, *, num_customers: int, num_vehicles: int, capacity: list[int],
                cost_ranges: int, tw_tightness: str, seed: int):
        
        self.num_customers = num_customers
        self.num_vehicles = num_vehicles
        self.capacity = capacity
        self.cost_low, self.cost_high = COST_RANGES[cost_ranges]
        self.tw_low, self.tw_high = TIME_WINDOW_TIGHTNESS[tw_tightness]
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.T_MAX = 10 * num_customers # Largo temporal en el que se desarolla la simulacion

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

        tij = cost_matrix.copy()

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