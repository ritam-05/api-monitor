from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from api.core.database import Base

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)
    method = Column(String, default="GET")
    timeout = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))