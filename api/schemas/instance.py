from pydantic import BaseModel


class SolveRequest(BaseModel):
    instance_id: str
    name: str
    V: int
    CUSTOMERS: int
    cost_matrix: list[list[float]]
    tij: list[list[float]]
    ei: list[float]
    li: list[float]
    F: list[float]
    Q: list[float]
    demands: list[float]
    callback_url: str | None = None  # overrides execution.yaml if provided


class SolveResponse(BaseModel):
    instance_id: str
    status: str = "queued"
