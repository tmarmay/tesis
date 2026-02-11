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
        "MILP": MILPSolver(cfg_milp=cfg.solvers.milp)
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
        runner = ExperimentRunner(experiment=exp, solvers=solvers, instance_reps=cfg.experiments['instance_reps'], timeout=cfg.experiments['timeout'])
        runner.run()
        return
    # ------------------------
    # NORMAL EXECUTION
    # ------------------------
    # Acá va tu código normal:
    # simulaciones, solvers, etc.
    # print("Running normal simulation...")

    #print help
    # from tests.test_capacity_demand import test_sufficient_capacity
    # test_sufficient_capacity()

if __name__ == "__main__":
    main()
