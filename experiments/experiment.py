from models.problem_instance import ProblemInstance
from typing import Iterator, Tuple
import subprocess

class Experiment:
    """
    Define un experimento reproducible.
    NO ejecuta solvers.
    NO guarda resultados.
    SOLO define qué instancias existen y cómo se identifican.
    """

    def __init__(self, *, name: str, generator, num_instances: int, base_seed: int = 42):
        """
        name: nombre lógico del experimento
        generator: SyntheticGenerator
        num_instances: cantidad de instancias a generar
        base_seed: semilla base para reproducibilidad
        """
        self.name = name
        self.generator = generator
        self.num_instances = num_instances
        self.base_seed = base_seed

    def _git_short_hash(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode("utf-8").strip()
        except Exception:
            return "nogit"

    def experiment_id(self) -> str:
        """
        ID lógico y reproducible del experimento.

        Cambia si cambia:
        - el nombre del experimento
        - la semilla base
        - la versión del código (commit de git)

        Esto evita mezclar resultados entre distintas versiones del modelo.
        """
        git_id = self._git_short_hash()
        return f"{self.name}__seed{self.base_seed}__git{git_id}"

    def instance_id(self, idx: int) -> str:
        """
        ID determinístico de una instancia dentro del experimento.
        """
        return f"{self.experiment_id()}__i{idx}"

    def iter_instances(self) -> Iterator[Tuple[str, ProblemInstance]]:
        """
        Iterador sobre las instancias del experimento.

        Yields:
            (instance_id, ProblemInstance)
        """
        for i in range(self.num_instances):

            seed = self.base_seed + i
            instance = self.generator.generate()

            yield self.instance_id(i), instance

    def generate_instances(self) -> list[Tuple[str, ProblemInstance]]:
        """
        Genera TODAS las instancias en memoria.
        Útil para tests o experimentos chicos.
        """
        return list(self.iter_instances())

    def __str__(self) -> str:
        return (
            f"Experiment(name={self.name}, "
            f"num_instances={self.num_instances}, "
            f"base_seed={self.base_seed})"
        )