from helpers.pretty_print import *
from models.solutions import Solution
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from validators.solution_validator import SolutionChecker

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

    def __init__(self, *,instance_id: str, instance: ProblemInstance, solver: BaseSolver, timeout: Optional[int] = None):
        """
        instance: ProblemInstance
        solver: solver obj
        timeout: maximum time for the solver to solve problem instance 
        """
        self.instance_id = instance_id
        self.instance = instance
        self.solver = solver
        self.timeout = timeout
        self.results = []

    def run(self) -> None:
        """
        Ejecuta todos los solvers sobre todas las instancias
        """
        if self.timeout is not None:
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(int(self.timeout))
        
        solution, runtime, errormsg = None, np.inf, ""
        try:
            start = time()
            solution = self.solver.solve(self.instance)
            runtime = time() - start
            status = "finished"

        except TimeoutException:
            status = "timeout"
            runtime = time() - start
            warning_pp(f"Solver {self.solver.get_solver_name()} timeout")

        except Exception as e:
            status = "error"
            errormsg = str(e)
            error_pp(f"Solver {self.solver.get_solver_name()}: error {errormsg}")

        finally:
            if self.timeout is not None:
                signal.alarm(0)
            if solution is None:
                solution = Solution(total_cost=np.inf, feasible=False, unserved_customers=self.instance.C, routes={})

            valid = False
            if solution.feasible:
                schecker = SolutionChecker(insta=self.instance)
                valid = schecker.check(solution.routes, self.solver.get_solver_name())

            self.results.append({
                "instance_id": self.instance_id,
                "solver": self.solver.get_solver_name(),
                "cost": solution.total_cost,
                "feasible": solution.feasible,
                "valid": valid,
                "runtime": runtime,
                "routes": solution.routes,
                "not_visited": solution.unserved_customers,
                "status": status,
                "error": errormsg
            })

    def get_results(self) -> list[dict]:
        return self.results
