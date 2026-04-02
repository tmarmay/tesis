from typing import Dict

import httpx

from models.problem_instance import ProblemInstance
from execution.strategies.base import BaseSolverStrategy
from storage.repository import save_result
from helpers.pretty_print import ok_pp, info_pp, error_pp
from execution.strategies.sequential import SequentialStrategy
from execution.strategies.parallel import ParallelStrategy


class ExecutionRunner:
    """
    Runs a single problem instance against a set of solvers and persists results.

    Designed to be called from:
    - CLI (execution mode in main.py)
    - FastAPI endpoint: run() is dispatched as a BackgroundTask; callback_url
      receives a POST with each solver result as it finishes.
    """
    def __init__(self, *, instance: dict, cfg: dict, solvers: Dict, id: str, callback_url_override: str | None = None):
        self.instance = self._load_instance_form_dict(instance)
        self.execution_id = id
        self.solvers = solvers
        self.strategy = self._get_strategy(cfg)
        self.timeout = self._get_timeout(cfg)
        self.callback_url = callback_url_override or cfg.execution['callback_url']

    def _get_callback_url(self, cfg) -> str | None:
        return cfg.execution['callback_url']

    def _get_timeout(self, cfg) -> int:
        return cfg.execution['timeout']

    def _get_strategy(self, cfg) -> BaseSolverStrategy:
        strategy_name = cfg.get("strategy", "sequential")
        if strategy_name == "sequential":
            strategy = SequentialStrategy()
        elif strategy_name == "parallel":
            strategy = ParallelStrategy()
        else:
            raise ValueError(f"Unknown strategy: '{strategy_name}'. Valid options: sequential, parallel.")        
        return strategy

    def _load_instance_form_dict(self, instance: dict) -> ProblemInstance:
        name = instance.get('name')
        V = instance.get('V')
        CUSTOMERS = instance.get('CUSTOMERS')
        cij = instance.get('cost_matrix')
        tij = instance.get('tij')
        ei = instance.get('ei')
        li = instance.get('li')
        F = instance.get('F')
        Q = instance.get('Q')
        demands = instance.get('demands')

        return ProblemInstance(name=name, V=V, CUSTOMERS=CUSTOMERS, cost_matrix=cij,
                               tij=tij, ei=ei, li=li, F=F, Q=Q, demands=demands)


    def run(self) -> list[dict]:
        info_pp(f"Starting execution: {self.execution_id}")

        results = self.strategy.run(
            instance=self.instance,
            solvers=self.solvers,
            timeout=self.timeout,
        )

        for result in results:
            try:
                save_result(
                    experiment_id="execution",
                    instance_id=self.execution_id,
                    instance_repetition=0,
                    result=result,
                )
                ok_pp(f"[SAVED] {self.execution_id} | {result['solver']}")
            except Exception as e:
                import traceback
                error_pp(f"[DB ERROR] {self.execution_id} | {result['solver']}: {e}")
                traceback.print_exc()

            if self.callback_url:
                self._notify(result)
        return results

    def results_2_json(self, results: list[dict]) -> list[dict]:
        """Returns results formatted for JSON export (e.g. HTTP response or file)."""
        def _sanitize(value):
            """Replace non-finite floats with None for JSON compliance."""
            import math
            if isinstance(value, float) and not math.isfinite(value):
                return None
            return value

        return [
            {
                "execution_id": self.execution_id,
                "solver": r["solver"],
                "status": r["status"],
                "feasible": r.get("feasible"),
                "valid": r.get("valid"),
                "cost": _sanitize(r["cost"]),
                "runtime": _sanitize(r["runtime"]),
                "routes": r.get("routes"),
                "not_visited": r.get("not_visited"),
                "error": r.get("error"),
            }
            for r in results
        ]

    def _notify(self, result: dict) -> None:
        payload = self.results_2_json([result])[0]
        try:
            httpx.post(self.callback_url, json=payload, timeout=10)
        except Exception as e:
            error_pp(f"[CALLBACK] Failed to notify {self.callback_url}: {e}")
