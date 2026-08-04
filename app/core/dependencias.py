from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.service.auth_service import verificar_token

_esquema_bearer = HTTPBearer()


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(_esquema_bearer)
) -> dict:
    token = credenciales.credentials
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="No autorizado.")

    return payload


def solo_admin(usuario: dict = Depends(usuario_actual)) -> dict:
    """
    Dependencia para proteger rutas SOLO para administradores.
    Úsala en vez de usuario_actual cuando la ruta sea exclusiva de admin.
    """
    categoria = (usuario.get("categoria") or "").strip().lower()

    if categoria != "admin":
        raise HTTPException(
            status_code=403,
            detail="Esta acción solo está disponible para administradores."
        )

    return usuario