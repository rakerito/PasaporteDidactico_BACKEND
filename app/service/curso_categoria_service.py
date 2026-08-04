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