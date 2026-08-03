from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.service.auth_service import verificar_token

_esquema_bearer = HTTPBearer()


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(_esquema_bearer)
) -> dict:
    """
    Dependencia para proteger rutas. Úsala así en cualquier endpoint:

        @router.get("/ruta-protegida")
        def mi_ruta(usuario: dict = Depends(usuario_actual)):
            ...

    'usuario' contendrá el payload del token: id_usuario (sub), correo, categoria.
    """
    token = credenciales.credentials
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="No autorizado."
        )

    return payload