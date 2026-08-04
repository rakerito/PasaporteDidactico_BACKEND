from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_curso)


# =====================================
# CONSULTAS
# =====================================

def obtener_por_id(id_curso: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_curso", id_curso)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar curso: {e}"
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
            detail=f"Error al listar cursos: {e}"
        )


def buscar(nombre: str):
    try:
        res = (
            _table()
            .select("*")
            .ilike("nombre", f"%{nombre}%")
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar cursos: {e}"
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
            detail=f"Error al crear curso: {e}"
        )


def actualizar(id_curso: int, datos: dict):
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
            .eq("id_curso", id_curso)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar curso: {e}"
        )


def eliminar(id_curso: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_curso", id_curso)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar curso: {e}"
        )

def listar_por_categoria(id_categoria: int):
    """
    Regresa los cursos completos que pertenecen a una categoría dada.
    """
    from app.service import curso_categoria_service

    ids_curso = curso_categoria_service.cursos_de_categoria_ids(id_categoria)

    if not ids_curso:
        return []

    try:
        res = (
            _table()
            .select("*")
            .in_("id_curso", ids_curso)
            .execute()
        )
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cursos por categoría: {e}")