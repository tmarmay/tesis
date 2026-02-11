# tests/test_time_windows.py

from data.instances.time_windows_infeacible import *
from data.instances.time_windows_feacible import *
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation

solvers = {
    "MILP": MILPSolver(),
    "ACO": ACOSolver(),
    "NearestNeighbor": NearestNeighborSolver(),
}

def test_infeacible():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_infeacible",
            instance=infeacible,
            solver=solver
        )
        sim.run()
        result = sim.get_results()[0]
    
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

def test_feacible():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_feacible",
            instance=feacible,
            solver=solver
        )
        sim.run()
        result = sim.get_results()[0]
        
        print("\n-----------------------------")
        print(f"Solver: {result['solver']}")
        print(f"Factible: {result['feasible']}")
        print(f"Costo: {result['cost']}")
        print(f"No visitados: {result['not_visited']}")
        print(f"Rutas: {result['routes']}")

        assert result["feasible"], (
            f"{result['solver']}: la solución fue marcada como infactible "
            f"cuando debería ser factible"
        )

        assert len(result["not_visited"]) == 0, (
            f"{result['solver']}: se detectaron clientes no visitados "
            f"en un caso donde debería visitrse todos"
        )

        print(f"{feacible.name} pasó para {result['solver']}")

