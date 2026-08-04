from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_docente)


# =====================================
# CONSULTAS
# =====================================

def obtener_por_id(id_docente: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_docente", id_docente)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar docente: {e}"
        )


def obtener_por_usuario(id_usuario1: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_usuario1", id_usuario1)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar docente por usuario: {e}"
        )


def listar():
    try:
        res = (
            _table()
            .select("*")
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar docentes: {e}"
        )


def listar_por_division(division: str):
    try:
        res = (
            _table()
            .select("*")
            .ilike("division", f"%{division}%")
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar docentes por división: {e}"
        )


# =====================================
# CRUD
# =====================================

def crear(datos: dict):
    try:
        if not datos:
            raise HTTPException(
                status_code=400,
                detail="No se recibieron datos."
            )

        # Un usuario solo debería tener un perfil de docente
        existe = obtener_por_usuario(datos["id_usuario1"])

        if existe:
            raise HTTPException(
                status_code=409,
                detail="Este usuario ya tiene un perfil de docente."
            )

        datos = jsonable_encoder(datos)

        res = (
            _table()
            .insert(datos)
            .execute()
        )
        return res.data[0]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear docente: {e}"
        )


def actualizar(id_docente: int, datos: dict):
    try:
        if not datos:
            raise HTTPException(
                status_code=400,
                detail="No se recibieron datos."
            )

        datos = jsonable_encoder(datos)

        res = (
            _table()
            .update(datos)
            .eq("id_docente", id_docente)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar docente: {e}"
        )


def eliminar(id_docente: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_docente", id_docente)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar docente: {e}"
        )