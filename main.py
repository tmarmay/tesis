from solvers.nearest_neighborhood import NearestNeighborSolver
from solvers.aco import ACOSolver
from solvers.aco_v2 import ACOSolverV2
from solvers.milp2a1 import MILPSolver

from storage.db import engine
from storage.models import Base
import hydra

# Seconds reserved for the MILP process to extract and return its solution
# after the solver hits its internal time limit, before the OS kills the subprocess.
_MILP_TIMEOUT_MARGIN = 180

def ants_it_estimator(params):
    return 28, 0
    if params['num_customers'] <= 25:
       return 100,300
    return 100, 300

def handle_milp_solvers(cfg_milp, timeout=None) -> dict:
    instances = {}
    if cfg_milp.solver == 'all':
        for solver_name, _ in cfg_milp.solvers.items():
            instances[solver_name] = MILPSolver(cfg_milp={'solver': solver_name, 'time_limit': timeout})
        return instances
    else:
        return {cfg_milp.solver: MILPSolver(cfg_milp={'solver': cfg_milp.solver, 'time_limit': timeout})}

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

        ants, it = ants_it_estimator(cfg.experiments)
        cfg.solvers.aco['num_ants'] = ants
        cfg.solvers.aco['num_iter'] = it
        solvers = {
            #"NearestNeighbor": NearestNeighborSolver(),
            #"ACO": ACOSolver(cfg_aco=cfg.solvers.aco),
            #"ACOv2": ACOSolverV2(cfg_aco=cfg.solvers.aco),
        }
        solvers = solvers | handle_milp_solvers(cfg.solvers.milp, timeout=cfg.experiments['timeout'])

        gen = SyntheticGenerator(cfg_experiment=cfg.experiments, cfg_generator=cfg.generator)
        exp = Experiment(name=cfg.experiments['name'], generator=gen, num_instances=cfg.experiments['num_instances'])
        runner = ExperimentRunner(experiment=exp, solvers=solvers, instance_reps=cfg.experiments['instance_reps'], timeout=cfg.experiments['timeout'] + _MILP_TIMEOUT_MARGIN, parallel_reps=cfg.experiments.get('parallel_reps', False), memory_limit_mb=cfg.experiments.get('memory_limit_mb'), reserved_cpus=cfg.experiments.get('reserved_cpus', 2))
        runner.run()
        return

    # ------------------------
    # EXECUTION MODE
    # ------------------------
    if mode == "execution":
        from execution.runner import ExecutionRunner
        from datetime import date

        base_timeout = cfg.execution['timeout']
        cfg.execution['timeout'] = base_timeout + _MILP_TIMEOUT_MARGIN
        ants, it = ants_it_estimator(cfg.execution)
        cfg.solvers.aco['num_ants'] = ants
        cfg.solvers.aco['num_iter'] = it
        solvers = {
            "NearestNeighbor": NearestNeighborSolver(),
            "ACO": ACOSolver(cfg_aco=cfg.solvers.aco),
        }
        solvers = solvers | handle_milp_solvers(cfg.solvers.milp, timeout=base_timeout)

        instance = None
        if cfg.execution['source_type'] == 'json':
            from helpers.io import load_instance_from_json
            instance = load_instance_from_json(cfg.execution.source)
        elif cfg.execution['source_type'] == 'POST':
            import uvicorn
            from api.app import create_app
            app = create_app(cfg=cfg, solvers=solvers)
            uvicorn.run(app, host="0.0.0.0", port=8001)
            return
        else:
            return

        execution_id = f"C{instance['CUSTOMERS']}_V{instance['V']}_{date.today().strftime('%Y%m%d')}"
        runner = ExecutionRunner(instance=instance, cfg=cfg, solvers=solvers, id=execution_id)
        runner.run()
        return

if __name__ == "__main__":
    main()
