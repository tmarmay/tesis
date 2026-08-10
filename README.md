## Tesis: Asignación Óptima de Viajes para Transporte de Maquinaria Agrícola con Restricciones Temporales y Operativas

#### Tomas Marmay ~ Famaf 2025-2026

### Proyecto: Resolución del MD-VRP-TW

Este proyecto implementa y compara distintos enfoques para resolver el **Problema de Ruteo de Vehículos con Múltiples Depósitos y Ventanas de Tiempo (MD-VRP-TW)**.
El objetivo es construir un **framework experimental modular**, que permita evaluar heurísticas, metaheurísticas y modelos exactos bajo instancias comunes y comparables.

### Descripción del problema

El MD-VRP-TW consiste en determinar un conjunto de rutas para una flota de vehículos que:

- parten desde múltiples depósitos
- deben atender un conjunto de clientes
- respetan ventanas de tiempo en los clientes
- regresan a un nodo de retorno (posiblemente distinto del depósito)
- minimizan el costo total (distancia + penalización por uso de vehículos)

Cada vehículo está asociado a un depósito y, opcionalmente, a un nodo de retorno distinto.

Se comparan tres enfoques: una heurística **Nearest Neighbor** (baseline), una metaheurística **ACO** (Ant Colony Optimization) y un modelo exacto **MILP**, usado como referencia óptima para instancias pequeñas.

---

### Dónde está cada cosa

#### La tesis

| Qué | Dónde |
|---|---|
| Documento final de la tesis | [`thesis/Tesis-Final.pdf`](thesis/Tesis-Final.pdf) |
| Diapositivas de la defensa oral | [`thesis/presentation/`](thesis/presentation/) (`Tesis-Presentacion.pptx` y `.pdf`) |
| Resultados de los experimentos que fueron al informe | [`thesis/database/run_results.sqlite`](thesis/database/run_results.sqlite) (tabla `run_results`), filtrada a las instancias con `experiment_id` que empieza con `turing8_`. Se regenera con `python scripts/build_results_db.py` a partir del dump completo de PostgreSQL `run_results.sql` (no está en el repo por tamaño, ~154MB, es local) |
| Notas de preparación de la defensa | [`Tesis Presentacion/`](Tesis%20Presentacion/) (vault de Obsidian) |
| Papers de referencia | [`papers/`](papers/), listado y descripción en [`papers/README.md`](papers/README.md) |

#### El código del framework

| Carpeta | Contenido |
|---|---|
| [`models/`](models/) | Estructuras del dominio (`ProblemInstance`, `Solution`) |
| [`solvers/`](solvers/) | Nearest Neighbor, ACO y MILP |
| [`simulations/`](simulations/) | Corre todos los solvers sobre todas las instancias |
| [`execution/`](execution/) y [`api/`](api/) | Ejecución de una instancia puntual (JSON o API) |
| [`data/`](data/) | Instancias e instancias de ejemplo (`data/instances/`) |
| [`conf/`](conf/) | Configuración de experimentos ([Hydra](https://hydra.cc/)) |
| [`analysis/exploratory/`](analysis/exploratory/) | Notebooks de exploración inicial de resultados |
| [`analysis/report/`](analysis/report/) | Notebooks que generaron las figuras/tablas del informe |
| [`main.py`](main.py) | Punto de entrada del framework |

Para el detalle de cómo está armada cada una de estas carpetas, instalación, cómo correr experimentos/tests y profiling, ver **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**.

#### Documentación adicional

- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) — instalación, arquitectura y cómo correr el proyecto
- [docs/RUNNING_FROM_JSON.md](docs/RUNNING_FROM_JSON.md) — ejecutar una instancia puntual
- [docs/TESTS.md](docs/TESTS.md) — tests
- [docs/API.md](docs/API.md) — API
- [docs/REMOTE.md](docs/REMOTE.md) — ejecución remota

