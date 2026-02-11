# tests/cost.py

from data.instances.cost_sum import *
from data.instances.cheap_route import *
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation

solvers = {
    "MILP": MILPSolver(),
    "ACO": ACOSolver(),
    "NearestNeighbor": NearestNeighborSolver(),
}

def test_cost_sum():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_cost_sum",
            instance=cost_sum,
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
            f"en un caso donde debería visitarse todos los vecinos"
        )

        assert result['cost'] == 41, (
            f"{result['solver']}: el costo no es el esperado "
            f"el costo es de {result['cost']} cuando deberia ser 41"
        )

        print(f"{cost_sum.name} pasó para {result['solver']}")

def test_cheap_route():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_cheap_route",
            instance=cheaper_route,
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
            f"en un caso donde debería visitarse todos los vecinos"
        )

        assert result['cost'] == 31, (
            f"{result['solver']}: el costo no es el esperado "
            f"el costo es de {result['cost']} cuando deberia ser 41"
        )

        print(f"{cheaper_route.name} pasó para {result['solver']}")
