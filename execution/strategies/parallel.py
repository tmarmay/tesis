from .base import BaseSolverStrategy


class ParallelStrategy(BaseSolverStrategy):
    """
    Runs all solvers concurrently on the same instance.

    Not yet implemented — reserved for future use.
    Consider memory constraints before enabling: each solver
    (especially MILP) can consume significant RAM.
    """

    def run(self, instance, solvers, timeout):
        raise NotImplementedError(
            "ParallelStrategy is not yet implemented. Use SequentialStrategy instead."
        )
