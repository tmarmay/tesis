from simulations.simulation import Simulation
from storage.repository import *
from helpers.pretty_print import * 

from typing import Dict, Optional

class ExperimentRunner:
    """
    Ejecuta un experimento completo:
    - itera instancias
    - corre solvers
    - persiste resultados incrementalmente
    - saltea corridas ya hechas
    - maneja timeouts
    """

    def __init__(self, *, experiment, solvers: Dict[str, object], instance_reps: int, timeout: Optional[int] = None):
        """
        experiment: Experiment
        solvers: dict {solver_name: solver_object}
        timeout: segundos máximos por solver (None = sin límite)
        """
        self.experiment = experiment
        self.solvers = solvers
        self.instance_repetitions = instance_reps 
        self.timeout = timeout
    
    def __get_solver_instnace_reps(self, solver) -> int:
        if solver.is_stochastic():
            return self.instance_repetitions
        return 1
    
    def _already_run(self, experiment_id, instance_id, solver) -> bool:
        return already_run(experiment_id=experiment_id, instance_id=instance_id, solver=solver)

    def _save_result(self, result: dict) -> None:
        for i in range(len(result['experiment'])):
            save_result(result['experiment_id'], 
                        result['instance_id'],
                        result['instance_repetition'],
                        result['experiment'][i])

    def run(self):
        experiment_id = self.experiment.experiment_id()

        info_pp(f"Running experiment: {experiment_id}")

        for instance_id, instance in self.experiment.iter_instances():
            result = {}

            print(f"\n{'*'*60}")
            print(f"  Begin Instance {instance_id}")
            print(f"{'*'*60}\n")
            
            for _, solver in self.solvers.items():

                if self._already_run(experiment_id, instance_id, solver.get_solver_name()):
                    ok_pp(f"[SKIP] {instance_id} - {solver.get_solver_name()} (already run)")
                    continue
                ok_pp(f"[RUN] {instance_id} - {solver.get_solver_name()}")

                print(f"\n{'='*40}")
                print(f"  Solving using {solver.get_solver_name()}...")
                print(f"{'='*40}\n")
                
                solver_reps = self.__get_solver_instnace_reps(solver)
                for k in range(solver_reps):
                    sim = Simulation(instance_id=instance_id, instance=instance, solver=solver, timeout=self.timeout)
                    sim.run()
                    sim_results = sim.get_results()

                    result['experiment_id'] = experiment_id
                    result['instance_id'] = instance_id
                    result['experiment'] = sim_results
                    result['instance_repetition'] = k
                    self._save_result(result)

        ok_pp("Experiment finished.")
