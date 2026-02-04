from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, JSON
from datetime import datetime

from storage.db import Base

class RunResult(Base):
    __tablename__ = "run_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    experiment_id = Column(String, index=True)
    instance_id = Column(String, index=True)
    solver = Column(String, index=True)

    status = Column(String)  # finished / timeout / error
    feasible = Column(Boolean)

    cost = Column(Float)
    runtime = Column(Float)

    routes = Column(JSON)
    not_visited = Column(JSON)

    created_at = Column(DateTime, default=datetime.now)