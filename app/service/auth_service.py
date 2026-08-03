from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from app.core.config import config
from app.service import usuario_service
from app.service.encryptar import verify_password


# =====================================
# LOGIN
# =====================================

def iniciar_sesion(correo: str, contraseña: str):
    try:
        usuario = usuario_service.obtener_por_correo(correo)

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos."
            )

        if not verify_password(contraseña, usuario["contraseña"]):
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos."
            )

        token = _generar_token(usuario)

        # No regresamos la contraseña (ni su hash) al cliente
        usuario_sin_contraseña = {
            k: v for k, v in usuario.items() if k != "contraseña"
        }

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": usuario_sin_contraseña
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al iniciar sesión: {e}"
        )


# =====================================
# TOKENS
# =====================================

def _generar_token(usuario: dict) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=config.jwt_expiration_minutes
    )

    payload = {
        "sub": str(usuario["id_usuario"]),
        "correo": usuario["correo"],
        "categoria": usuario["categoria"],
        "exp": expiracion
    }

    return jwt.encode(
        payload,
        config.jwt_secret_key,
        algorithm=config.jwt_algorithm
    )


def verificar_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            config.jwt_secret_key,
            algorithms=[config.jwt_algorithm]
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="La sesión ha expirado, inicia sesión de nuevo."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )