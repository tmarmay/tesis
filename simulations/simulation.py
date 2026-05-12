from helpers.pretty_print import error_pp, warning_pp
from models.solutions import Solution
from solvers.base_solver import BaseSolver
from models.problem_instance import ProblemInstance
from validators.solution_validator import SolutionChecker

import multiprocessing
import threading
import resource
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from time import time, sleep
import numpy as np
import psutil
import os

# 'spawn' starts a fresh interpreter per subprocess — no inherited locks,
# no FD leaks between concurrent forks, and no loky .env conflict.
_MP_CTX = multiprocessing.get_context('spawn')


def _rep_worker(solver, instance, conn) -> None:
    """Runs in a subprocess. Measures CPU/RAM, builds the full result dict."""
    proc = psutil.Process(os.getpid())
    proc.cpu_percent(interval=None)  # initialize CPU counter

    solution, status, errormsg = None, "error", ""
    start = time()
    try:
        solution = solver.solve(instance)
        status = "finished"
    except Exception as e:
        status = "error"
        errormsg = str(e)
    finally:
        runtime = time() - start
        cpu_usage = proc.cpu_percent(interval=None)
        ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB → MB

        if solution is None:
            solution = Solution(total_cost=np.inf, feasible=False,
                                unserved_customers=instance.C, routes={})

        valid = False
        if solution.feasible:
            checker = SolutionChecker(insta=instance)
            valid = checker.check(solution.routes, solver.get_solver_name())

        conn.send({
            "solver": solver.get_solver_name(),
            "cost": solution.total_cost,
            "reference_cost": instance.reference_cost,
            "feasible": solution.feasible,
            "valid": valid,
            "status": status,
            "runtime": runtime,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "c": instance.CUSTOMERS,
            "v": instance.V,
            **solver.get_run_params(),
            "routes": solution.routes if solution.routes else None,
            "not_visited": solution.unserved_customers,
            "error": errormsg,
        })
        conn.close()


def _dead_result(solver, instance, status: str, runtime: float, error: str = "") -> dict:
    return {
        "solver": solver.get_solver_name(),
        "cost": np.inf,
        "reference_cost": instance.reference_cost,
        "feasible": False,
        "valid": False,
        "status": status,
        "runtime": runtime,
        "cpu_usage": None,
        "ram_usage": None,
        "c": instance.CUSTOMERS,
        "v": instance.V,
        "routes": None,
        "not_visited": instance.C,
        "error": error,
    }


def run_rep(solver, instance, timeout: Optional[int],
            memory_limit_mb: Optional[int] = None) -> dict:
    """Spawns one subprocess for a single solver run. Enforces timeout and RAM limit."""
    effective_timeout = timeout if timeout and timeout > 0 else None
    parent_conn, child_conn = _MP_CTX.Pipe(duplex=False)
    p = _MP_CTX.Process(target=_rep_worker, args=(solver, instance, child_conn))
    start = time()
    p.start()
    child_conn.close()  # parent doesn't write, close its copy of the write end

    oom_triggered = threading.Event()

    def _memory_watchdog():
        try:
            proc = psutil.Process(p.pid)
            while p.is_alive():
                rss_mb = proc.memory_info().rss / 1024 / 1024
                if rss_mb > memory_limit_mb:
                    p.kill()
                    oom_triggered.set()
                    return
                sleep(1)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if memory_limit_mb:
        watchdog = threading.Thread(target=_memory_watchdog, daemon=True)
        watchdog.start()

    p.join(timeout=effective_timeout)

    if oom_triggered.is_set():
        parent_conn.close()
        error_pp(f"Solver {solver.get_solver_name()}: killed (RAM limit {memory_limit_mb}MB exceeded)")
        return _dead_result(solver, instance, "error", time() - start,
                            f"RAM limit exceeded ({memory_limit_mb}MB)")

    if p.is_alive():
        p.terminate()
        p.join()
        parent_conn.close()
        warning_pp(f"Solver {solver.get_solver_name()} timeout")
        return _dead_result(solver, instance, "timeout", time() - start)

    if p.exitcode != 0:
        parent_conn.close()
        error_pp(f"Solver {solver.get_solver_name()}: worker exited with code {p.exitcode}")
        return _dead_result(solver, instance, "error", time() - start,
                            f"worker exited with code {p.exitcode}")

    try:
        result = parent_conn.recv()
    except Exception as e:
        result = _dead_result(solver, instance, "error", time() - start, str(e))
    finally:
        parent_conn.close()

    return result


class Simulation:
    """Direct (in-process) solver execution. Used by SequentialStrategy (execution mode)."""

    def __init__(self, *, instance_id: str, instance: ProblemInstance, solver: BaseSolver,
                 timeout: Optional[int] = None):
        self.instance_id = instance_id
        self.instance = instance
        self.solver = solver
        self.timeout = timeout
        self.results = []

    def run(self) -> None:
        solution, status, errormsg = None, "error", ""
        start = time()
        try:
            solution = self.solver.solve(self.instance)
            status = "finished"
        except Exception as e:
            status = "error"
            errormsg = str(e)
            error_pp(f"Solver {self.solver.get_solver_name()}: error {errormsg}")
        finally:
            runtime = time() - start
            ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB → MB
            if solution is None:
                solution = Solution(total_cost=np.inf, feasible=False,
                                    unserved_customers=self.instance.C, routes={})
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
                "ram_usage": ram_usage,
                "routes": solution.routes,
                "not_visited": solution.unserved_customers,
                "status": status,
                "error": errormsg,
            })

    def get_results(self) -> list[dict]:
        return self.results
