import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Try to get Vercel's Postgres URL, fallback to standard DATABASE_URL, finally fallback to local SQLite
DATABASE_URL = os.getenv("POSTGRES_URL", os.getenv("DATABASE_URL", "sqlite:///./api_monitor.db"))

# 2. SQLAlchemy > 1.4 requires the URL to start with postgresql:// instead of postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()