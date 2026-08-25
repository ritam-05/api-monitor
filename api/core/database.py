import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# We use SQLite for local development. In production, Vercel will provide a Postgres URL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./api_monitor.db")

# The connect_args dictionary is needed ONLY for SQLite to allow multiple threads.
# If we are using Postgres, we don't pass this argument.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function to yield a database session for each request,
    ensuring the session is closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()