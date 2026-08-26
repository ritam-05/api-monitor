from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from api.core.database import Base

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # <--- NEW
    name = Column(String, index=True)
    url = Column(String)
    method = Column(String, default="GET")
    timeout = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())