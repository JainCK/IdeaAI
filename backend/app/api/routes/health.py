import time
from fastapi import APIRouter

from app.api.models.response import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "timestamp": time.time()}