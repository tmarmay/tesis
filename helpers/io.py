import json

from models.problem_instance import ProblemInstance

def load_instance_from_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

def save_instance_as_json(instance: ProblemInstance, path: str) -> None:
    data = {
        "name": instance.name,
        "V": instance.V,
        "CUSTOMERS": instance.CUSTOMERS,
        "cost_matrix": instance.cost_matrix.tolist() if hasattr(instance.cost_matrix, 'tolist') else instance.cost_matrix,
        "tij": instance.tij.tolist() if hasattr(instance.tij, 'tolist') else instance.tij,
        "ei": instance.ei,
        "li": instance.li,
        "F": instance.F,
        "demands": instance.demands,
        "Q": instance.Q,
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)