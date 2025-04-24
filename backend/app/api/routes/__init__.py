from fastapi import FastAPI
from app.api.routes.ideas import router as ideas_router
from app.api.routes.search import router as search_router
from app.api.routes.feedback import router as feedback_router
from app.api.routes.health import router as health_router
from app.core.config import settings

def register_routes(app: FastAPI):
    """Register all API routes."""
    app.include_router(ideas_router, prefix=settings.API_V1_STR)
    app.include_router(search_router, prefix=settings.API_V1_STR)
    app.include_router(feedback_router, prefix=settings.API_V1_STR)
    app.include_router(health_router, prefix=settings.API_V1_STR)