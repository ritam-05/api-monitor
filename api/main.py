from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.database import engine, Base
from api.models import endpoint, result  # <-- Update: Added result model
from api.routes import endpoints
from api.routes import engine as engine_router 

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Monitor",
    description="Backend for the API Monitoring Dashboard",
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)
app.include_router(engine_router.router) 

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}