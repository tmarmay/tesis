# Tests

## Running tests

```bash
# Run the full test suite
python -m pytest

# Run tests from a single file
python3 -m pytest tests/<file>.py

# Run a single test
python3 -m pytest tests/<file>.py::<test_fun>
```

## Examples

```bash
python3 -m pytest tests/test_cost.py::test_cost_sum
```
