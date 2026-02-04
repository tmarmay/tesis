# simulations/simulation.py

from typing import List, Dict
from time import time


class Simulation:
    """
    Orquestador de experimentos.
    Corre múltiples solvers sobre múltiples instancias
    y guarda los resultados.
    """

    def __init__(self, instances: list, solvers: dict):
        """
        instances: list de ProblemInstance
        solvers: dict {solver_name: solver_object}
        """
        self.instances = instances
        self.solvers = solvers
        self.results = []

    def run(self) -> None:
        """
        Ejecuta todos los solvers sobre todas las instancias
        """
        for inst_id, instance in enumerate(self.instances):

            for solver_name, solver in self.solvers.items():

                start = time()
                solution = solver.solve(instance)
                runtime = time() - start

                self.results.append({
                    "instance_id": inst_id,
                    "solver": solver_name,
                    "cost": solution.total_cost,
                    "feasible": solution.feasible,
                    "runtime": runtime,
                    "routes": solution.routes,
                    "not_visited": solution.unserved_customers
                })

    def get_results(self) -> list[dict]:
        return self.results
