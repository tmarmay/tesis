from fastapi import APIRouter, BackgroundTasks

from api.schemas.instance import SolveRequest, SolveResponse
from execution.runner import ExecutionRunner


def build_router(cfg, solvers: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/solve", response_model=SolveResponse, status_code=200)
    def solve(request: SolveRequest, background_tasks: BackgroundTasks):
        instance = request.model_dump(exclude={"callback_url", "instance_id"})
        instance_id = request.instance_id

        callback_url = request.callback_url or cfg.execution["callback_url"]

        runner = ExecutionRunner(
            instance=instance,
            cfg=cfg,
            solvers=solvers,
            id=instance_id,
            callback_url_override=callback_url,
        )
        background_tasks.add_task(runner.run)

        return SolveResponse(instance_id=instance_id)

    return router
