from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MonitoringResultResponse(BaseModel):
    id: int
    endpoint_id: int
    is_success: bool
    status_code: Optional[int] = None
    response_time_ms: float
    error_message: Optional[str] = None
    checked_at: datetime

    class Config:
        from_attributes = True