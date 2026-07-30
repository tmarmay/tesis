# models/solution.py

class Solution:
    """
    Representa una solución del MD-VRP-TW.
    """

    def __init__(self, routes: dict, total_cost: float, feasible:bool, unserved_customers=None, timed_out:bool=False):
        """
        routes: dict {depot: [nodos en orden]}
        total_cost: float
        feasible: bool
        unserved_customers: list (opcional)
        timed_out: True si el solver paró por time limit (solución feasible pero no óptima)
        """
        self.routes = routes
        self.total_cost = total_cost
        self.feasible = feasible
        self.unserved_customers = unserved_customers or []
        self.timed_out = timed_out

    def __repr__(self):
        return (
            f"Solution(cost={self.total_cost:.2f}, "
            f"feasible={self.feasible}, "
            f"unserved={len(self.unserved_customers)})"
        )
