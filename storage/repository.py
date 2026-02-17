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
            cost=cost,
            runtime=result.get("runtime"),
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


def already_run(experiment_id: int, instance_id: int) -> bool:
    db = SessionLocal()
    exists = db.query(RunResult).filter(
        RunResult.experiment_id == experiment_id,
        RunResult.instance_id == instance_id,
        RunResult.status == "finished"
    ).first() is not None
    db.close()
    return exists