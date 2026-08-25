from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from api.core.database import Base

class MonitoringResult(Base):
    __tablename__ = "monitoring_results"

    id = Column(Integer, primary_key=True, index=True)
    # The ondelete="CASCADE" ensures if we delete an endpoint, its history is also deleted
    endpoint_id = Column(Integer, ForeignKey("endpoints.id", ondelete="CASCADE"), index=True, nullable=False)
    
    is_success = Column(Boolean, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=False)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)