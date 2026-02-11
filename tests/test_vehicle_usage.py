# tests/vehicule_usage.py

from data.instances.single_vehicle_required_for_feasibility import *
from data.instances.two_vehicle_required_for_feasibility import *
from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver
from simulations.simulation import Simulation

solvers = {
    "MILP": MILPSolver(),
    "ACO": ACOSolver(),
    "NearestNeighbor": NearestNeighborSolver(),
}

def test_single_vehicle_required():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_single_vehicle_required",
            instance=single_vehicle_required,
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

        if result['solver'] == "NearestNeighbor":
            print("Este solver no es capaz de resolver este test por limitacion de diseño")
            continue
        
        assert len(result["not_visited"]) == 0, (
            f"{result['solver']}: se detectaron clientes no visitados "
            f"en un caso donde debería visitarse todos los vecinos"
        )
        
        assert len(result['routes']) == 1, (
            f"{result['solver']}: rompe una ventana de tiempo "
            f"el solver deberia usar un solo vehiculo"
        )

        print(f"{single_vehicle_required.name} pasó para {result['solver']}")

def test_two_vehicle_required():
    for s_name, solver in solvers.items():
        sim = Simulation(
            instance_id="test_two_vehicle_required",
            instance=two_vehicle_required,
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

        assert len(result['routes']) == 2, (
            f"{result['solver']}: no se puede resolver con un solo vehiculo"
            f"es necesario dos vehiculos para resolver esta instancia"
        )
        
        print(f"{two_vehicle_required.name} pasó para {result['solver']}")


