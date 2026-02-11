# tests/capacity_demand.py

from data.instances.more_demand_than_capacity import *
from data.instances.more_capacity_than_demand import *
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation

solvers = {
    "MILP": MILPSolver(),
    "ACO": ACOSolver(),
    "NearestNeighbor": NearestNeighborSolver(),
}

def test_insufficient_capacity():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_insufficient_capacity",
            instance=infeasible_cause_capacity,
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
            f"cuando debería ser infactible por falta de capacidad"
        )

        print(f"{infeasible_cause_capacity.name} pasó para {result['solver']}")

def test_insufficient_capacity2():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_insufficient_capacity2",
            instance=infeasible_cause_capacity2,
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
            f"cuando debería ser infactible por falta de capacidad"
        )

        print(f"{infeasible_cause_capacity2.name} pasó para {result['solver']}")

def test_sufficient_capacity():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_sufficient_capacity",
            instance=feasible_cause_capacity,
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
            f"cuando debería ser factible porque sobra capacidad"
        )

        print(f"{feasible_cause_capacity.name} pasó para {result['solver']}")


def test_sufficient_capacity2():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_sufficient_capacity2",
            instance=feasible_cause_capacity2,
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
            f"cuando debería ser factible porque sobra capacidad"
        )

        print(f"{feasible_cause_capacity2.name} pasó para {result['solver']}")


