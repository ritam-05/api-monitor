from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import asyncio

from api.core.database import get_db
from api.models.endpoint import Endpoint
from api.models.result import MonitoringResult
from api.services.monitor import check_endpoint

router = APIRouter(
    prefix="/api/engine",
    tags=["Monitoring Engine"]
)

# Vercel Cron sends GET requests, our UI sends POST. We support both!
@router.get("/run-checks")
@router.post("/run-checks")
async def run_monitoring_checks(db: Session = Depends(get_db)):
    active_endpoints = db.query(Endpoint).filter(Endpoint.is_active == True).all()
    
    if not active_endpoints:
        return {"message": "No active endpoints to monitor.", "results": []}
        
    async def check_and_format(ep: Endpoint):
        check_result = await check_endpoint(url=ep.url, method=ep.method, timeout=ep.timeout)
        return {
            "endpoint_id": ep.id,
            "name": ep.name,
            "url": ep.url,
            **check_result
        }

    tasks = [check_and_format(ep) for ep in active_endpoints]
    check_results = await asyncio.gather(*tasks)
    
    for res in check_results:
        db_result = MonitoringResult(
            endpoint_id=res["endpoint_id"],
            is_success=res["is_success"],
            status_code=res["status_code"],
            response_time_ms=res["response_time_ms"],
            error_message=res["error_message"]
        )
        db.add(db_result)
        
    db.commit() 
    
    return {
        "message": f"Successfully checked {len(active_endpoints)} endpoints and saved results.",
        "results": check_results
    }