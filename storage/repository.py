from storage.db import SessionLocal
from storage.models import RunResult

def save_result(experiment_id: int, instance_id: int, status: str, result: dict) -> None:
    db = SessionLocal()

    run = RunResult(
        experiment_id=experiment_id,
        instance_id=instance_id,
        status=status,
        solver=result["solver"],
        feasible=result.get("feasible"),
        cost=result.get("cost"),
        runtime=result.get("runtime"),
        routes=result.get("routes"),
        not_visited=result.get("not_visited"),
    )

    db.add(run)
    db.commit()
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