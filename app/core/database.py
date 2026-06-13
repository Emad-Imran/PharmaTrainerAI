import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

engine_options = {
    "connect_args": {"check_same_thread": False},
}

if DATABASE_URL == "sqlite:///:memory:":
    engine_options["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_database_session():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()