from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_requiere)


# =====================================
# CONSULTAS
# =====================================

def obtener(id_curso2: int, id_sello1: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_curso2", id_curso2)
            .eq("id_sello1", id_sello1)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar requisito: {e}"
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
            detail=f"Error al listar requisitos: {e}"
        )


def listar_por_curso(id_curso2: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_curso2", id_curso2)
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar requisitos del curso: {e}"
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

        existe = obtener(datos["id_curso2"], datos["id_sello1"])

        if existe:
            raise HTTPException(
                status_code=409,
                detail="Ese curso ya requiere ese sello."
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
            detail=f"Error al crear requisito: {e}"
        )


def eliminar(id_curso2: int, id_sello1: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_curso2", id_curso2)
            .eq("id_sello1", id_sello1)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar requisito: {e}"
        )