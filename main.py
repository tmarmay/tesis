from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.milp2a1 import MILPSolver

from storage.db import engine
from storage.models import Base
import hydra

#ver como mejorar esto
def timeout_estimator(params):
    pred_params = params['runtime_prediction']
    return int(pred_params['safety_factor'] * (params['num_customers'] ** pred_params['alpha']) * (params['num_vehicles'] ** pred_params['beta']))

def ants_it_estimator(params):
    if params['num_customers'] <= 50:
        return 100,100
    return 200, 300
Base.metadata.create_all(bind=engine)

@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def main(cfg):
    cfg.experiments['timeout'] = timeout_estimator(cfg.experiments)
    ants, it = ants_it_estimator(cfg.experiments)
    cfg.solvers.aco['num_ants'] = ants
    cfg.solvers.aco['num_iter'] = it

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
