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

from tests.test_time_windows import *
test_infeacible()