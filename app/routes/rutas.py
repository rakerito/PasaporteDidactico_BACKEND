from fastapi import APIRouter
from app.routes import health

router = APIRouter()

# Registrar rutas de sub-módulos
router.include_router(health.router, tags=["Health"])

@router.get("/", tags=["Root"])
def bienvenida():
    return {
        "message": "Bienvenido a la API de Pasaporte Didáctico",
        "docs": "/docs"
    }
