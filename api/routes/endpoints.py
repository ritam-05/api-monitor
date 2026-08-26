from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.core.database import get_db
from api.models.endpoint import Endpoint
from api.models.result import MonitoringResult
from api.schemas.endpoint import EndpointCreate, EndpointUpdate, EndpointResponse
from api.schemas.result import MonitoringResultResponse

router = APIRouter(
    prefix="/api/endpoints",
    tags=["Endpoints"]
)

# Notice these are now "" instead of "/"
@router.post("", response_model=EndpointResponse)
def create_endpoint(endpoint: EndpointCreate, db: Session = Depends(get_db)):
    db_endpoint = Endpoint(**endpoint.model_dump())
    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint

@router.get("", response_model=List[EndpointResponse])
def read_endpoints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    endpoints = db.query(Endpoint).offset(skip).limit(limit).all()
    return endpoints

@router.get("/{endpoint_id}", response_model=EndpointResponse)
def read_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return db_endpoint

@router.put("/{endpoint_id}", response_model=EndpointResponse)
def update_endpoint(endpoint_id: int, endpoint: EndpointUpdate, db: Session = Depends(get_db)):
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    update_data = endpoint.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_endpoint, key, value)
        
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint

@router.delete("/{endpoint_id}")
def delete_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    db.delete(db_endpoint)
    db.commit()
    return {"ok": True, "message": "Endpoint deleted successfully"}

@router.get("/{endpoint_id}/results", response_model=List[MonitoringResultResponse])
def read_endpoint_results(endpoint_id: int, limit: int = 50, db: Session = Depends(get_db)):
    db_endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
        
    results = db.query(MonitoringResult)\
        .filter(MonitoringResult.endpoint_id == endpoint_id)\
        .order_by(MonitoringResult.checked_at.desc())\
        .limit(limit)\
        .all()
        
    return results