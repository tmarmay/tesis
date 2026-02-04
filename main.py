from models.problem_instance import ProblemInstance
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation

from storage.db import engine
from storage.models import Base

Base.metadata.create_all(bind=engine)

solvers = {
    "NearestNeighbor": NearestNeighborSolver(),
    "ACO": ACOSolver(),
    "MILP": MILPSolver()
}


# import argparse
# import subprocess
# import sys


# def run_pytest(target: str | None):
#     """
#     Ejecuta pytest.
#     - Si target es None -> corre todos los tests
#     - Si target existe -> se lo pasa directo a pytest
#     """
#     cmd = [sys.executable, "-m", "pytest"]

#     if target:
#         cmd.append(target)

#     subprocess.run(cmd, check=False)
#     sys.exit(0)


# def main():
#     parser = argparse.ArgumentParser(
#         description="MD-VRP-TW Simulator & Test Runner"
#     )

#     parser.add_argument(
#         "--test",
#         nargs="?",
#         const="",
#         metavar="PYTEST_TARGET",
#         help=(
#             "Run pytest. Optional target:\n"
#             "  --test                      (all tests)\n"
#             "  --test test_time_windows    (single file)\n"
#             "  --test test_file::test_name (single test)"
#         ),
#     )

#     args = parser.parse_args()

#     # ------------------------
#     # TEST MODE
#     # ------------------------
#     if args.test is not None:
#         target = args.test if args.test != "" else None
#         run_pytest(target)

#     # ------------------------
#     # NORMAL EXECUTION
#     # ------------------------
#     # Acá va tu código normal:
#     # simulaciones, solvers, etc.
#     # print("Running normal simulation...")
#     # ...


# if __name__ == "__main__":
#     main()

from data.generators.synthetic import SyntheticGenerator
from experiments.experiment import Experiment
from experiments.runner import ExperimentRunner

gen = SyntheticGenerator(num_customers=3, num_vehicles=2, capacity=[1,5],cost_ranges=2, tw_tightness='critical', seed=42)
exp = Experiment(name="second run", generator=gen, num_instances=5)
runner = ExperimentRunner(experiment=exp, solvers=solvers, timeout=None)
runner.run()