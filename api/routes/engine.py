from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import asyncio

from api.core.database import get_db
from api.models.endpoint import Endpoint
from api.services.monitor import check_endpoint

router = APIRouter(
    prefix="/api/engine",
    tags=["Monitoring Engine"]
)

@router.post("/run-checks")
async def run_monitoring_checks(db: Session = Depends(get_db)):
    """
    Trigger a health check for all active endpoints.
    In production, this will be called by a Vercel Cron Job.
    """
    # 1. Fetch all active endpoints from the database
    active_endpoints = db.query(Endpoint).filter(Endpoint.is_active == True).all()
    
    if not active_endpoints:
        return {"message": "No active endpoints to monitor.", "results": []}
        
    # 2. Define a helper function to wrap the check and format the output
    async def check_and_format(ep: Endpoint):
        check_result = await check_endpoint(url=ep.url, method=ep.method, timeout=ep.timeout)
        return {
            "endpoint_id": ep.id,
            "name": ep.name,
            "url": ep.url,
            **check_result
        }

    # 3. Run all checks concurrently using asyncio.gather for speed
    tasks = [check_and_format(ep) for ep in active_endpoints]
    check_results = await asyncio.gather(*tasks)
    
    # (In Phase 6, we will add the code here to save these results to the database!)
    
    return {
        "message": f"Successfully checked {len(active_endpoints)} endpoints.",
        "results": check_results
    }