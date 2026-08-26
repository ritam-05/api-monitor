from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EndpointBase(BaseModel):
    name: str
    url: str
    method: str = "GET"
    timeout: int = 5
    is_active: bool = True

class EndpointCreate(EndpointBase):
    pass

class EndpointUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    timeout: Optional[int] = None
    is_active: Optional[bool] = None

class EndpointResponse(EndpointBase):
    id: int
    user_id: str # <--- NEW
    created_at: datetime

    class Config:
        from_attributes = True