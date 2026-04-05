# Running vrp-core from a JSON instance

Use this to run or debug a specific instance without going through the full experiment pipeline.

## Command

```bash
python main.py mode=execution execution.source_type=json execution.source=/path/to/instance.json
```

To run a specific solver instead of all:
```bash
python main.py mode=execution execution.source_type=json execution.source=/path/to/instance.json execution.solver=ACO
```

---

## Option 1: Generate a JSON from the synthetic generator

```bash
ipython
```
```python
from hydra import compose, initialize_config_dir
import os

with initialize_config_dir(config_dir=os.path.abspath("conf"), version_base="1.3"):
    cfg = compose(config_name="config", overrides=["mode=simulation"])

from data.generators.synthetic import SyntheticGenerator
from helpers.io import save_instance_as_json

gen = SyntheticGenerator(cfg_experiment=cfg.execution, cfg_generator=cfg.generator)
pi = gen.generate()
save_instance_as_json(pi, "single-execution-example.json")
```

---

## Option 2: Capture an instance from shelter-plataform

Set `VRP_CORE_DEBUG_DUMP = True` in shelter-plataform's `settings.py`. The next job dispatched will be saved as `debug_instance_job_<id>.json` in the project's `BASE_DIR`. Copy that file here and run with the command above.
