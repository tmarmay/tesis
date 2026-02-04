# models/problem_instance.py

class ProblemInstance:
    """
    Representa una instancia del MD-VRP-TW.
    Contiene SOLO datos del problema.
    """

    def __init__(self, name: str, V: int, CUSTOMERS: int, cost_matrix: list,
                tij: list, ei: list, li: list, F: list, demands: list, Q: list):
        
        self.name = name

        self.V = V
        self.CUSTOMERS = CUSTOMERS

        self.cost_matrix = cost_matrix
        self.tij = tij

        self.ei = ei
        self.li = li
        self.F = F

        self.Q = Q # capacidad máxima del vehículo.
        # Para que funcione con numeros mayores a 1 hay que hacer una modificacion
        self.demands = [1 for _ in range(CUSTOMERS)] #Demenda de cada customer i

        self.service_time = [0 for _ in range(CUSTOMERS)]

        self.N = CUSTOMERS + 2*V
        self.C = [i for i in range(CUSTOMERS)] #CUSTOMERS
        self.DEPOTS = [i for i in range(self.C[-1] + 1, self.C[-1] + 1 + V)]
        self.RETURNS_milp = [i for i in range(self.C[-1] + V + 1, self.N)]

        self.RETURNS = { #no me gusta porq difiere de milp, verificar mas adalente
            self.DEPOTS[v]: self.C[-1] + 1 + V + v
            for v in range(V)
        }

    def __str__(self) -> str:
        lines = []
        lines.append(f"ProblemInstance: {self.name}")
        lines.append("-" * 40)
        lines.append(f"Vehicles: {self.V}")
        lines.append(f"Customers: {self.CUSTOMERS}")
        lines.append(f"Total nodes: {self.N}")


        lines.append("")
        lines.append(f"Customers: {list(self.C)}")
        lines.append(f"Depots: {self.DEPOTS}")
        lines.append(f"Returns: {list(self.RETURNS.values())}")

        lines.append("")
        lines.append(f"Vehicle capacities (Q): {self.Q}")
        lines.append(f"Fixed costs (F): {self.F}")

        # ventanas de tiempo de customers (resumen)
        tw_customers = [
            (self.ei[c], self.li[c]) for c in self.C
        ]
        lines.append("")
        lines.append("Customer time windows (ei, li):")
        for c, (ei, li) in zip(self.C, tw_customers):
            lines.append(f"  Customer {c}: [{ei}, {li}]")

        # info matrices (solo tamaño)
        lines.append("")
        lines.append(f"Cost matrix shape: {len(self.cost_matrix)} x {len(self.cost_matrix[0])}")
        lines.append(f"Travel time matrix shape: {len(self.tij)} x {len(self.tij[0])}")

        return "\n".join(lines)
