from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_categoria)


def obtener_por_id(id_categoria: int):
    try:
        res = _table().select("*").eq("id_categoria", id_categoria).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar categoría: {e}")


def listar():
    try:
        res = _table().select("*").execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar categorías: {e}")


def crear(datos: dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="No se recibieron datos.")
        datos = jsonable_encoder(datos)
        res = _table().insert(datos).execute()
        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear categoría: {e}")


def actualizar(id_categoria: int, datos: dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="No se recibieron datos.")
        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id_categoria", id_categoria).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar categoría: {e}")


def eliminar(id_categoria: int):
    try:
        res = _table().delete().eq("id_categoria", id_categoria).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar categoría: {e}")