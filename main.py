from models.problem_instance import ProblemInstance
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation


# solvers = {
#     "NearestNeighbor": NearestNeighborSolver(),
#     "ACO": ACOSolver(),
#     "MILP": MILPSolver()
# }

# #LA IDEA ES NO USAR SETTINGS PERO POR AHORA LO HAGO ASI
# from solvers.sim_settings import *
# instance = ProblemInstance(
#     name="toy_instance",
#     V=2,
#     CUSTOMERS=CUSTOMERS,
#     cost_matrix=cost_matrix,
#     tij=tij,
#     ei=ei,
#     li=li,
#     F=F,
#     demands=demands,
#     Q=Q
# )

# sim = Simulation(
#     instances=[instance],
#     solvers=solvers
# )
# sim.run()
# results = sim.get_results()

# for r in results:
#     print(f"Solver: {r['solver']}")
#     print(f"  Costo: {r['cost']}")
#     print(f"  Factible: {r['feasible']}")
#     print(f"  Rutas: {r['routes']}")
#     print()



import argparse
import subprocess
import sys


def run_pytest(target: str | None):
    """
    Ejecuta pytest.
    - Si target es None -> corre todos los tests
    - Si target existe -> se lo pasa directo a pytest
    """
    cmd = [sys.executable, "-m", "pytest"]

    if target:
        cmd.append(target)

    subprocess.run(cmd, check=False)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="VRP Simulator & Test Runner"
    )

    parser.add_argument(
        "--test",
        nargs="?",
        const="",
        metavar="PYTEST_TARGET",
        help=(
            "Run pytest. Optional target:\n"
            "  --test                      (all tests)\n"
            "  --test test_time_windows    (single file)\n"
            "  --test test_file::test_name (single test)"
        ),
    )

    args = parser.parse_args()

    # ------------------------
    # TEST MODE
    # ------------------------
    if args.test is not None:
        target = args.test if args.test != "" else None
        run_pytest(target)

    # ------------------------
    # NORMAL EXECUTION
    # ------------------------
    # Acá va tu código normal:
    # simulaciones, solvers, etc.
    # print("Running normal simulation...")
    # ...


if __name__ == "__main__":
    main()
