from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_otorga)


# =====================================
# CONSULTAS
# =====================================

def obtener_por_id(id_otorgar: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_otorgar", id_otorgar)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar otorgamiento: {e}"
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
            detail=f"Error al listar otorgamientos: {e}"
        )


def listar_por_usuario(id_usuario1: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_usuario1", id_usuario1)
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar otorgamientos del usuario: {e}"
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
            detail=f"Error al crear otorgamiento: {e}"
        )


def actualizar(id_otorgar: int, datos: dict):
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
            .eq("id_otorgar", id_otorgar)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar otorgamiento: {e}"
        )


def eliminar(id_otorgar: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_otorgar", id_otorgar)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar otorgamiento: {e}"
        )