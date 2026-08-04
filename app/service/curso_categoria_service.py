from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_curso_categoria)


def listar_por_curso(id_curso: int):
    try:
        res = _table().select("*").eq("id_curso", id_curso).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar categorías del curso: {e}")


def listar_por_categoria(id_categoria: int):
    try:
        res = _table().select("*").eq("id_categoria", id_categoria).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar cursos de la categoría: {e}")


def asignar(id_curso: int, id_categoria: int):
    try:
        existe = (
            _table()
            .select("*")
            .eq("id_curso", id_curso)
            .eq("id_categoria", id_categoria)
            .execute()
        )
        if existe.data:
            raise HTTPException(status_code=409, detail="Ese curso ya tiene asignada esa categoría.")

        datos = jsonable_encoder({"id_curso": id_curso, "id_categoria": id_categoria})
        res = _table().insert(datos).execute()
        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al asignar categoría: {e}")


def quitar(id_curso: int, id_categoria: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_curso", id_curso)
            .eq("id_categoria", id_categoria)
            .execute()
        )
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al quitar categoría: {e}")

def categorias_de_curso_detalle(id_curso: int):
    """
    Regresa las categorías (con nombre) asignadas a un curso,
    no solo los ids crudos de la tabla de unión.
    """
    from app.service import categoria_service

    relaciones = listar_por_curso(id_curso)
    ids_categoria = [r["id_categoria"] for r in relaciones]

    if not ids_categoria:
        return []

    try:
        sb = get_supabase()
        res = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_categoria)
            .select("*")
            .in_("id_categoria", ids_categoria)
            .execute()
        )
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar categorías del curso: {e}")

def cursos_de_categoria_ids(id_categoria: int) -> list[int]:
    relaciones = listar_por_categoria(id_categoria)
    return [r["id_curso"] for r in relaciones]