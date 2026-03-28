from typing import Dict, Optional

from models.problem_instance import ProblemInstance
from simulations.simulation import Simulation

from .base import BaseSolverStrategy


class SequentialStrategy(BaseSolverStrategy):
    """Runs each solver one after another on the same instance."""

    def run(self, instance: ProblemInstance, solvers: Dict, timeout: Optional[int]) -> list[dict]:
        results = []
        for _, solver in solvers.items():
            sim = Simulation(
                instance_id=instance.name,
                instance=instance,
                solver=solver,
                timeout=timeout,
            )
            sim.run()
            results.extend(sim.get_results())
        return results
