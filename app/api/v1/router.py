from fastapi import APIRouter
from app.api.v1.endpoints import health

api_router = APIRouter()

# Registrar sub-routers de endpoints
api_router.include_router(health.router, tags=["Health"])
