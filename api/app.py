from fastapi import FastAPI

from api.routes.vrp import build_router


def create_app(cfg, solvers: dict) -> FastAPI:
    app = FastAPI(title="VRP CORE")
    app.include_router(build_router(cfg=cfg, solvers=solvers))
    return app
