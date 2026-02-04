from simulations.simulation import Simulation
from storage.repository import *

import json
import os
import signal
from typing import Dict, Optional


class TimeoutException(Exception):
    print("Solver timeout")


def _timeout_handler(signum, frame):
    raise TimeoutException()


class ExperimentRunner:
    """
    Ejecuta un experimento completo:
    - itera instancias
    - corre solvers
    - persiste resultados incrementalmente
    - saltea corridas ya hechas
    - maneja timeouts
    """

    def __init__(self, *, experiment, solvers: Dict[str, object], timeout: Optional[int] = None):
        """
        experiment: Experiment
        solvers: dict {solver_name: solver_object}
        timeout: segundos máximos por solver (None = sin límite)
        """
        self.experiment = experiment
        self.solvers = solvers
        self.timeout = timeout


    def _already_run(self, experiment_id, instance_id) -> bool:
        return already_run(experiment_id=experiment_id, instance_id=instance_id)

    def _save_result(self, result: dict) -> None:
        for i in range(len(result['experiment'])):
            save_result(result['experiment_id'], 
                        result['instance_id'], 
                        result['status'], 
                        result['experiment'][i])

    def run(self):
        experiment_id = self.experiment.experiment_id()

        print(f"Running experiment: {experiment_id}")

        for instance_id, instance in self.experiment.iter_instances():
            result = {}

            if self._already_run(experiment_id, instance_id): #no tiene en cuenta el solver
                print(f"[SKIP] {instance_id} (already run)")
                continue

            print(f"[RUN] {instance_id}")
            status = "running"

            try:
                if self.timeout is not None:
                    signal.signal(signal.SIGALRM, _timeout_handler)
                    signal.alarm(int(self.timeout))

                sim = Simulation(instances=[instance], solvers=self.solvers)
                sim.run()
                sim_results = sim.get_results()
                status = "finished"

            except TimeoutException:
                status = "timeout"

            except Exception as e:
                status = "error"
                error_msg = str(e)

            finally:
                if self.timeout is not None:
                    signal.alarm(0)

            result['experiment_id'] = experiment_id
            result['instance_id'] = instance_id
            result['status'] = status
            result['experiment'] = sim_results

            if status == "error":
                result['error'] = error_msg

            self._save_result(result)

        print("Experiment finished.")
