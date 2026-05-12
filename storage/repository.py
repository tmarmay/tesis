from storage.db import SessionLocal
from storage.models import RunResult
import math

def save_result(experiment_id: int, instance_id: int, instance_repetition: int, result: dict) -> None:
    db = SessionLocal()
    try:
        cost = 0 if math.isinf(result.get("cost")) else int(result.get("cost"))

        run = RunResult(
            experiment_id=experiment_id,
            instance_id=instance_id,
            instance_repetition=instance_repetition,
            status=result["status"],
            solver=result["solver"],
            feasible=result.get("feasible"),
            valid=result.get("valid"),
            cost=cost,
            reference_cost=result.get("reference_cost"),
            runtime=result.get("runtime"),
            c=result.get("c"),
            v=result.get("v"),
            ram_usage=result.get("ram_usage"),
            cpu_usage=result.get("cpu_usage"),
            ants=result.get("ants"),
            it=result.get("it"),
            routes=result.get("routes") if result.get("routes") else None,
            not_visited=list(result.get("not_visited")),
        )
        db.add(run)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def already_run(experiment_id: int, instance_id: int, solver: str) -> bool:
    db = SessionLocal()
    exists = db.query(RunResult).filter(
        RunResult.experiment_id == experiment_id,
        RunResult.instance_id == instance_id,
        RunResult.solver == solver  
    ).first() is not None
    db.close()
    return exists