from pydantic import BaseModel
from datetime import datetime

# Shared properties
class EndpointBase(BaseModel):
    name: str
    url: str
    method: str = "GET"
    timeout: int = 5
    is_active: bool = True

# Properties to receive on endpoint creation
class EndpointCreate(EndpointBase):
    pass

# Properties to receive on endpoint update
class EndpointUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    method: str | None = None
    timeout: int | None = None
    is_active: bool | None = None

# Properties to return to the client
class EndpointResponse(EndpointBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True