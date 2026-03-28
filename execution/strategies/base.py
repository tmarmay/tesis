from abc import ABC, abstractmethod
from typing import Dict, Optional

from models.problem_instance import ProblemInstance
from solvers.base_solver import BaseSolver


class BaseSolverStrategy(ABC):
    @abstractmethod
    def run(
        self,
        instance: ProblemInstance,
        solvers: Dict[str, BaseSolver],
        timeout: Optional[int],
    ) -> list[dict]:
        ...
