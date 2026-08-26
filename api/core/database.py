import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 1. Check for custom SUPABASE_DB_URL first, then fallbacks
DATABASE_URL = os.getenv("SUPABASE_DB_URL", os.getenv("POSTGRES_URL", os.getenv("DATABASE_URL", "sqlite:///./api_monitor.db")))

# 2. Ensure SQLAlchemy uses postgresql:// instead of postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Serverless Configuration: Use NullPool for live Postgres to handle function cold-starts
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # NullPool prevents connection leaks and drops in Vercel serverless functions
    engine = create_engine(DATABASE_URL, poolclass=NullPool)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()