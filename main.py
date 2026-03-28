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

def handle_milp_solvers(cfg_milp) -> dict:
    instances = {}
    if cfg_milp.solver == 'all':
        for solver_name, _ in cfg_milp.solvers.items():
            instances = instances | {solver_name: MILPSolver(cfg_milp={'solver': solver_name})}
        return instances
    else:
        return {cfg_milp['solver']: MILPSolver(cfg_milp=cfg_milp)}

Base.metadata.create_all(bind=engine)

@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def main(cfg):
    mode = cfg.mode['mode']
    # ------------------------
    # SIMULATION MODE
    # ------------------------
    if mode == "simulation":
        from data.generators.synthetic import SyntheticGenerator
        from experiments.experiment import Experiment
        from experiments.runner import ExperimentRunner

        cfg.experiments['timeout'] = timeout_estimator(cfg.experiments)
        ants, it = ants_it_estimator(cfg.experiments)
        cfg.solvers.aco['num_ants'] = ants
        cfg.solvers.aco['num_iter'] = it
        solvers = {
            "NearestNeighbor": NearestNeighborSolver(),
            "ACO": ACOSolver(cfg_aco=cfg.solvers.aco),
        }
        solvers = solvers | handle_milp_solvers(cfg.solvers.milp)

        gen = SyntheticGenerator(cfg_experiment=cfg.experiments, cfg_generator=cfg.generator)
        exp = Experiment(name=cfg.experiments['name'], generator=gen, num_instances=cfg.experiments['num_instances'])
        runner = ExperimentRunner(experiment=exp, solvers=solvers, instance_reps=cfg.experiments['instance_reps'], timeout=cfg.experiments['timeout'])
        runner.run()
        return

    # ------------------------
    # EXECUTION MODE
    # ------------------------
    if mode == "execution":
        from execution.runner import ExecutionRunner
        from datetime import date

        cfg.execution['timeout'] = timeout_estimator(cfg.execution)
        ants, it = ants_it_estimator(cfg.execution)
        cfg.solvers.aco['num_ants'] = ants
        cfg.solvers.aco['num_iter'] = it
        solvers = {
            "NearestNeighbor": NearestNeighborSolver(),
            "ACO": ACOSolver(cfg_aco=cfg.solvers.aco),
        }
        solvers = solvers | handle_milp_solvers(cfg.solvers.milp)

        instance = None
        if cfg.execution['source_type'] == 'json':
            from helpers.io import load_instance_from_json
            instance = load_instance_from_json(cfg.execution.source)
        elif cfg.execution['source_type'] == 'POST':
            pass # not implemented yet
        else:
            return

        execution_id = f"C{instance['CUSTOMERS']}_V{instance['V']}_{date.today().strftime('%Y%m%d')}"
        runner = ExecutionRunner(instance=instance, cfg=cfg, solvers=solvers, id=execution_id)
        runner.run()
        return

if __name__ == "__main__":
    main()
