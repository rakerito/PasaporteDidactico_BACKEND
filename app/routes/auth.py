from fastapi import APIRouter

from app.models.usuario import iniciarUsuario
from app.service import auth_service

router = APIRouter()


@router.post("/auth/login", tags=["Autenticación"])
def login(datos: iniciarUsuario):
    return auth_service.iniciar_sesion(datos.correo, datos.contraseña)