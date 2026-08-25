from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.core.database import get_db
from api.models.endpoint import Endpoint
from api.schemas.endpoint import EndpointCreate, EndpointUpdate, EndpointResponse

# Create a router specifically for our /api/endpoints path
router = APIRouter(
    prefix="/api/endpoints",
    tags=["Endpoints"]
)

@router.post("/", response_model=EndpointResponse)
def create_endpoint(endpoint: EndpointCreate, db: Session = Depends(get_db)):
    """Add a new API endpoint to monitor."""
    # Convert Pydantic schema to SQLAlchemy model
    db_endpoint = Endpoint(**endpoint.model_dump())
    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint

@router.get("/", response_model=List[EndpointResponse])
def read_endpoints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all monitored API endpoints."""
    endpoints = db.query(Endpoint).offset(skip).limit(limit).all()
    return endpoints

@router.get("/{endpoint_id}", response_model=EndpointResponse)
def read_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    """Get details for a specific API endpoint."""
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return db_endpoint

@router.put("/{endpoint_id}", response_model=EndpointResponse)
def update_endpoint(endpoint_id: int, endpoint: EndpointUpdate, db: Session = Depends(get_db)):
    """Update an existing API endpoint."""
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    # Update only the fields that were provided
    update_data = endpoint.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_endpoint, key, value)
        
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint

@router.delete("/{endpoint_id}")
def delete_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    """Delete an API endpoint from monitoring."""
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    db.delete(db_endpoint)
    db.commit()
    return {"ok": True, "message": "Endpoint deleted successfully"}