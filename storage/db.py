from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = DATABASE_URL = "postgresql+psycopg2:///results"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()