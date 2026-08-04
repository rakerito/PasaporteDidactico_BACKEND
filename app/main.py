from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import rutas

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API para la aplicación móvil Flutter de Pasaporte Didáctico"
)

# Configuración de Middleware CORS para permitir peticiones desde la app Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar enrutador principal de app.routes.rutas
app.include_router(rutas.router)
