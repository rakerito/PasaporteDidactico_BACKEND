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

def obtener(id_sello2: int, id_constancia1: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_sello2", id_sello2)
            .eq("id_constancia1", id_constancia1)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar otorgamiento: {e}"
        )


def obtener_por_id(id_otorga: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_otorga", id_otorga)
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


def listar_por_constancia(id_constancia1: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_constancia1", id_constancia1)
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar otorgamientos de la constancia: {e}"
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

        existe = obtener(datos["id_sello2"], datos["id_constancia1"])

        if existe:
            raise HTTPException(
                status_code=409,
                detail="Esa constancia ya otorga ese sello."
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


def eliminar(id_otorga: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_otorga", id_otorga)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar otorgamiento: {e}"
        )