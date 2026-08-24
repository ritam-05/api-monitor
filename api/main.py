from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Monitor",
    description="Backend for the API Monitoring Dashboard",
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json"
)

# CORS configuration to allow our Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # We will restrict this to specific domains in Phase 11
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