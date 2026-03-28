from typing import Dict

from models.problem_instance import ProblemInstance
from execution.strategies.base import BaseSolverStrategy
from storage.repository import save_result
from helpers.pretty_print import ok_pp, info_pp
from execution.strategies.sequential import SequentialStrategy
from execution.strategies.parallel import ParallelStrategy


class ExecutionRunner:
    """
    Runs a single problem instance against a set of solvers and persists results.

    Designed to be called from:
    - CLI (execution mode in main.py)
    - FastAPI endpoint (future): wrap run() in an async task, pass callback_url
      to notify shelter-platform when each solver finishes.
    """
    def __init__(self, *, instance: dict, cfg: dict, solvers: Dict, id: str):
        self.instance = self._load_instance_form_dict(instance)
        self.execution_id = id
        self.solvers = solvers
        self.strategy = self._get_strategy(cfg)
        self.timeout = self._get_timeout(cfg)
        self.callback_url = self._get_callback_url(cfg)  # reserved for future FastAPI/webhook use

    def _get_callback_url(self, cfg) -> str:
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
            save_result(
                experiment_id="execution",
                instance_id=self.execution_id,
                instance_repetition=0,
                result=result,
            )
            ok_pp(f"[SAVED] {self.execution_id} | {result['solver']}")

            if self.callback_url:
                self._notify(result)
        return results

    def results_2_json(self, results: list[dict]) -> list[dict]:
        """Returns results formatted for JSON export (e.g. HTTP response or file)."""
        return [
            {
                "execution_id": self.execution_id,
                "solver": r["solver"],
                "status": r["status"],
                "feasible": r.get("feasible"),
                "valid": r.get("valid"),
                "cost": r["cost"],
                "runtime": r["runtime"],
                "routes": r.get("routes"),
                "not_visited": r.get("not_visited"),
            }
            for r in results
        ]

    def _notify(self, result: dict) -> None:
        # Future: POST result to callback_url when a solver finishes.
        # This is the hook that shelter-platform uses to emit a websocket event.
        #
        # import httpx
        # httpx.post(self.callback_url, json=self.export_results([result])[0])
        pass
