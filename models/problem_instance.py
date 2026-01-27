# models/problem_instance.py

class ProblemInstance:
    """
    Representa una instancia del MD-VRP-TW.
    Contiene SOLO datos del problema.
    """

    def __init__(self, name, V, CUSTOMERS, cost_matrix, tij, ei, li, F, demands, Q):
        self.name = name

        self.V = V
        self.CUSTOMERS = CUSTOMERS

        self.cost_matrix = cost_matrix
        self.tij = tij

        self.ei = ei
        self.li = li
        self.F = F

        self.Q = [2 for _ in range(V)] # capacidad máxima del vehículo.
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