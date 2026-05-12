from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, JSON
from datetime import datetime

from storage.db import Base

class RunResult(Base):
    __tablename__ = "run_results"

    id = Column(Integer, primary_key=True, autoincrement=True)

    experiment_id = Column(String, index=True)
    instance_id = Column(String, index=True)
    instance_repetition = Column(Integer)
    solver = Column(String, index=True)

    status = Column(String)  # finished / timeout / error
    feasible = Column(Boolean)
    valid = Column(Boolean, default=False)

    cost = Column(Float)
    reference_cost = Column(Float, nullable=True)
    runtime = Column(Float)

    c = Column(Integer, nullable=True)
    v = Column(Integer, nullable=True)
    ram_usage = Column(Float, nullable=True)   # MB
    cpu_usage = Column(Float, nullable=True)   # percent (0-100)
    ants = Column(Integer, nullable=True)
    it = Column(Integer, nullable=True)

    routes = Column(JSON)
    not_visited = Column(JSON)

    created_at = Column(DateTime, default=datetime.now)