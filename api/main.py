from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.database import engine, Base
from api.models import endpoint  # We import this so SQLAlchemy knows about the model

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Monitor",
    description="Backend for the API Monitoring Dashboard",
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json"
)

# CORS configuration to allow our Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    """
    Basic health check endpoint to verify the backend is running.
    """
    return {"status": "ok", "message": "Backend is running!"}