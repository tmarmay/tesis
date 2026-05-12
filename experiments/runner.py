from simulations.simulation import run_rep
from storage.repository import save_result, already_run
from helpers.pretty_print import ok_pp, info_pp

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Optional
import os


class ExperimentRunner:
    """
    Ejecuta un experimento completo:
    - itera instancias
    - corre solvers (con repeticiones secuenciales o paralelas)
    - persiste resultados incrementalmente
    - saltea corridas ya hechas
    - maneja timeouts y mide CPU/RAM por corrida
    """

    def __init__(self, *, experiment, solvers: Dict[str, object], instance_reps: int,
                 timeout: Optional[int] = None, parallel_reps: bool = False,
                 memory_limit_mb: Optional[int] = None, reserved_cpus: int = 2):
        self.experiment = experiment
        self.solvers = solvers
        self.instance_repetitions = instance_reps
        self.timeout = timeout
        self.parallel_reps = parallel_reps
        self.memory_limit_mb = memory_limit_mb
        self.max_workers = max(1, os.cpu_count() - reserved_cpus)

    def __get_solver_reps(self, solver) -> int:
        return self.instance_repetitions if solver.is_stochastic() else 1

    def _already_run(self, experiment_id, instance_id, solver) -> bool:
        return already_run(experiment_id=experiment_id, instance_id=instance_id, solver=solver)

    def _run_sequential(self, solver, instance, reps) -> list[dict]:
        results = []
        for k in range(reps):
            result = run_rep(solver, instance, self.timeout, self.memory_limit_mb)
            result['instance_repetition'] = k
            results.append(result)
        return results

    def _run_parallel(self, solver, instance, reps) -> list[dict]:
        """Runs reps concurrently up to max_workers. Each rep gets its own subprocess with timeout."""
        results = [None] * reps
        with ThreadPoolExecutor(max_workers=min(reps, self.max_workers)) as pool:
            futures = {pool.submit(run_rep, solver, instance, self.timeout, self.memory_limit_mb): k
                       for k in range(reps)}
            for future in as_completed(futures):
                k = futures[future]
                result = future.result()
                result['instance_repetition'] = k
                results[k] = result
        return results

    def run(self):
        experiment_id = self.experiment.experiment_id()
        info_pp(f"Running experiment: {experiment_id}")

        for instance_id, instance in self.experiment.iter_instances():
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

                reps = self.__get_solver_reps(solver)
                run_fn = self._run_parallel if self.parallel_reps and reps > 1 else self._run_sequential
                results = run_fn(solver, instance, reps)

                for result in results:
                    rep = result.pop('instance_repetition')
                    save_result(experiment_id, instance_id, rep, result)

        ok_pp("Experiment finished.")
