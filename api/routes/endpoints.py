from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.core.database import get_db
from api.models.endpoint import Endpoint
from api.schemas.endpoint import EndpointCreate, EndpointUpdate, EndpointResponse

# Create a router for all endpoint-related routes
router = APIRouter(
    prefix="/api/endpoints",
    tags=["Endpoints"]
)

@router.post("/", response_model=EndpointResponse, status_code=status.HTTP_201_CREATED)
def create_endpoint(endpoint_in: EndpointCreate, db: Session = Depends(get_db)):
    """Create a new API endpoint to monitor."""
    new_endpoint = Endpoint(**endpoint_in.model_dump())
    db.add(new_endpoint)
    db.commit()
    db.refresh(new_endpoint)
    return new_endpoint

@router.get("/", response_model=List[EndpointResponse])
def read_endpoints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all monitored API endpoints."""
    endpoints = db.query(Endpoint).offset(skip).limit(limit).all()
    return endpoints

@router.get("/{endpoint_id}", response_model=EndpointResponse)
def read_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific API endpoint by its ID."""
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return endpoint

@router.put("/{endpoint_id}", response_model=EndpointResponse)
def update_endpoint(endpoint_id: int, endpoint_in: EndpointUpdate, db: Session = Depends(get_db)):
    """Update a specific API endpoint."""
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    update_data = endpoint_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(endpoint, key, value)
        
    db.commit()
    db.refresh(endpoint)
    return endpoint

@router.delete("/{endpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    """Delete a specific API endpoint."""
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    db.delete(endpoint)
    db.commit()
    return None