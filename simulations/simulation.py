from helpers.pretty_print import *
from models.solutions import Solution

from typing import Optional
from time import time
import signal
import numpy as np

class TimeoutException(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutException()

class Simulation:
    """
    Orquestador de experimentos.
    Corre múltiples solvers sobre múltiples instancias
    y guarda los resultados.
    """

    def __init__(self, instances: list, solvers: dict, timeout: Optional[int] = None):
        """
        instances: list de ProblemInstance
        solvers: dict {solver_name: solver_object}
        timeout: maximum time for the solver to solve problem instance 
        """
        self.instances = instances
        self.solvers = solvers
        self.timeout = timeout
        self.results = []

    def run(self) -> None:
        """
        Ejecuta todos los solvers sobre todas las instancias
        """
        for inst_id, instance in enumerate(self.instances):

            for solver_name, solver in self.solvers.items():
                solution, runtime, errormsg = None, 0, ""
                if self.timeout is not None:
                    signal.signal(signal.SIGALRM, _timeout_handler)
                    signal.alarm(int(self.timeout))

                try:
                    start = time()
                    solution = solver.solve(instance)
                    runtime = time() - start
                    status = "finished"

                except TimeoutException:
                    status = "timeout"
                    warning_pp(f"Solver {solver_name} timeout")

                except Exception as e:
                    status = "error"
                    errormsg = str(e)
                    error_pp(f"Solver {solver_name}: error {errormsg}")

                finally:
                    if self.timeout is not None:
                        signal.alarm(0)
                    if solution is None:
                        solution = Solution(total_cost=np.inf, feasible=False, unserved_customers=instance.C, routes={})

                self.results.append({
                    "instance_id": inst_id,
                    "solver": solver_name,
                    "cost": solution.total_cost,
                    "feasible": solution.feasible,
                    "runtime": runtime,
                    "routes": solution.routes,
                    "not_visited": solution.unserved_customers,
                    "status": status,
                    "error": errormsg
                })

    def get_results(self) -> list[dict]:
        return self.results
