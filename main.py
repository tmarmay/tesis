from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver

from storage.db import engine
from storage.models import Base
import hydra

Base.metadata.create_all(bind=engine)

@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def main(cfg):
    solvers = {
        "NearestNeighbor": NearestNeighborSolver(),
        "ACO": ACOSolver(cfg_aco=cfg.solvers.aco),
        "MILP": MILPSolver()
    }

    # ------------------------
    # EXPERIMENT MODE
    # ------------------------
    if cfg.mode['mode'] == "simulation":
        from data.generators.synthetic import SyntheticGenerator
        from experiments.experiment import Experiment
        from experiments.runner import ExperimentRunner

        gen = SyntheticGenerator(cfg_experiment=cfg.experiments, cfg_generator=cfg.generator)
        exp = Experiment(name=cfg.experiments['name'], generator=gen, num_instances=cfg.experiments['num_instances'])
        runner = ExperimentRunner(experiment=exp, solvers=solvers, timeout=cfg.experiments['timeout'])
        runner.run()
        return
    # ------------------------
    # NORMAL EXECUTION
    # ------------------------
    # Acá va tu código normal:
    # simulaciones, solvers, etc.
    # print("Running normal simulation...")

    #print help

if __name__ == "__main__":
    main()

# from tests.test_big_feasible_problem import test_big_problem
# test_big_problem()