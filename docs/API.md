# VRP CORE — HTTP API

## Running the server

```bash
python main.py mode=execution execution.source_type=POST
```

Listens on `http://0.0.0.0:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## `POST /solve`

Queues a VRP instance for solving. Returns immediately with `200` — solving runs in the background.

```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d @single-execution-example.json
```

---

## Callback

When each solver finishes, the runner POSTs to `callback_url` with the result. One payload per solver, as they complete.

**Priority:**
1. `callback_url` field in the request body
2. `callback_url` in `conf/execution/execution.yaml`
3. If both are `null`, no notification is sent
