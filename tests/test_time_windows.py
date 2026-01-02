# tests/test_time_windows.py

from data.instances.time_windows_infeacible import *
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation

solvers = {
    "NearestNeighbor": NearestNeighborSolver(),
    "MILP": MILPSolver(),
    "ACO": ACOSolver()
}

def test_infeacible():
    sim = Simulation(
        instances=[infeacible],
        solvers=solvers
    )
    sim.run()
    results = sim.get_results()
    
    for result in results:
        print("\n-----------------------------")
        print(f"Solver: {result['solver']}")
        print(f"Factible: {result['feasible']}")
        print(f"Costo: {result['cost']}")
        print(f"No visitados: {result['not_visited']}")
        print(f"Rutas: {result['routes']}")

        assert not result["feasible"], (
            f"{result['solver']}: la solución fue marcada como factible "
            f"cuando debería ser infactible"
        )

        assert len(result["not_visited"]) > 0, (
            f"{result['solver']}: no se detectaron clientes no visitados "
            f"en un caso donde debería perderse al menos uno"
        )

        print(f"{infeacible.name} pasó para {result['solver']}")


# def test_loss_one_client():
#     sim = Simulation(
#         instances=[loss_one_client],
#         solvers=solvers
#     )
#     sim.run()
#     results = sim.get_results()
    
#     for result in results:
#         print("\n-----------------------------")
#         print(f"Solver: {result['solver']}")
#         print(f"Factible: {result['feasible']}")
#         print(f"Costo: {result['cost']}")
#         print(f"No visitados: {result['not_visited']}")
#         print(f"Rutas: {result['routes']}")

#         assert not result["feasible"], (
#             f"{result['solver']}: la solución fue marcada como factible "
#             f"cuando debería ser infactible"
#         )

#         assert len(result["not_visited"]) > 0, (
#             f"{result['solver']}: no se detectaron clientes no visitados "
#             f"en un caso donde debería perderse al menos uno"
#         )

#         print(f"test_loss_one_client pasó para {result['solver']}")

# def test_all_in_time():
#     sim = Simulation(
#         instances=[all_in_time],
#         solvers=solvers
#     )
#     sim.run()
#     results = sim.get_results()
    
#     for result in results:
#         print("\n-----------------------------")
#         print(f"Solver: {result['solver']}")
#         print(f"Factible: {result['feasible']}")
#         print(f"Costo: {result['cost']}")
#         print(f"No visitados: {result['not_visited']}")
#         print(f"Rutas: {result['routes']}")

#         assert not result["feasible"], (
#             f"{result['solver']}: la solución fue marcada como factible "
#             f"cuando debería ser infactible"
#         )

#         assert len(result["not_visited"]) > 0, (
#             f"{result['solver']}: no se detectaron clientes no visitados "
#             f"en un caso donde debería perderse al menos uno"
#         )

#         print(f"test_loss_one_client pasó para {result['solver']}")

